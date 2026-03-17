import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import argparse
from pathlib import Path

from bug import bug1, bug2
from utils import image_to_binary_matrix, select_start_end


def visualize_bug1_vs_bug2(
	matrix,
	path1,
	path2,
	start_pose,
	end_pose,
	*,
	total_time_s: float = 3.0,
	stride: int = 3,
):
	grid = np.array(matrix, dtype=np.uint8)

	if stride < 1:
		stride = 1

	MIN_INTERVAL_MS = 5
	max_frames = int(total_time_s * 1000 / MIN_INTERVAL_MS)

	longest = max(len(path1), len(path2))
	effective_stride = max(stride, -(-longest // max_frames))

	grid_disp = grid
	path1_disp = path1[::effective_stride]
	path2_disp = path2[::effective_stride]
	start_xy = (start_pose.x, start_pose.y)
	end_xy = (end_pose.x, end_pose.y)

	h, w = grid_disp.shape

	n_frames = max(1, max(len(path1_disp), len(path2_disp)))
	interval_ms = max(MIN_INTERVAL_MS, int((total_time_s * 1000.0) / n_frames))

	fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))

	def setup_ax(ax, title, color):
		ax.set_title(title)
		ax.set_aspect("equal")
		ax.set_xticks([])
		ax.set_yticks([])
		ax.grid(False)
		ax.imshow(grid_disp, cmap="gray_r", origin="upper", interpolation="nearest")

		s_dot, = ax.plot(start_xy[0], start_xy[1], "go", markersize=4, label="Start")
		e_dot, = ax.plot(end_xy[0], end_xy[1], "bo", markersize=4, label="End")
		robot, = ax.plot([], [], "o", color=color, markersize=4, label="Robot")
		trail, = ax.plot([], [], color=color, linewidth=1, alpha=0.6)

		ax.set_xlim(-0.5, w - 0.5)
		ax.set_ylim(h - 0.5, -0.5)

		ax.legend(loc="upper right")
		return s_dot, e_dot, robot, trail

	s1, e1, robot1, trail1 = setup_ax(ax1, f"Bug1  ({len(path1_disp)} steps)", "red")
	s2, e2, robot2, trail2 = setup_ax(ax2, f"Bug2  ({len(path2_disp)} steps)", "blue")

	xs1, ys1 = [], []
	xs2, ys2 = [], []

	def update(frame):
		idx1 = min(frame, len(path1_disp) - 1)
		x1, y1 = path1_disp[idx1]
		robot1.set_data([x1], [y1])
		if frame < len(path1_disp):
			xs1.append(x1)
			ys1.append(y1)
		trail1.set_data(xs1, ys1)

		idx2 = min(frame, len(path2_disp) - 1)
		x2, y2 = path2_disp[idx2]
		robot2.set_data([x2], [y2])
		if frame < len(path2_disp):
			xs2.append(x2)
			ys2.append(y2)
		trail2.set_data(xs2, ys2)

		return robot1, trail1, s1, e1, robot2, trail2, s2, e2

	ani = animation.FuncAnimation(
		fig,
		update,
		frames=n_frames,
		interval=interval_ms,
		blit=True,
		repeat=False,
	)
	plt.tight_layout()
	plt.show()
	return ani


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("image_path", nargs="?", default="images/Spirale.png")
	args = parser.parse_args()

	print("Usage: python3 visualization.py [image_path]")
	print("No file provided -> default: images/Spirale.png")
	images_dir = Path("images")
	if images_dir.is_dir():
		image_files = sorted(
			[
				path.name
				for path in images_dir.iterdir()
				if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".gif"}
			]
		)
		print("Available images in images/:")
		if image_files:
			for file_name in image_files:
				print(f" - {file_name}")
		else:
			print(" - (no image files found)")
	else:
		print("images/ directory not found")

	matrix = image_to_binary_matrix(args.image_path)

	start_pose, end_pose = select_start_end(matrix)

	print("Running Bug1...")
	path1 = bug1(matrix, robot_radius=10, start_pose=start_pose, end_pose=end_pose)
	print(f"  Bug1 path length: {len(path1)} steps")

	print("Running Bug2...")
	path2 = bug2(matrix, robot_radius=10, start_pose=start_pose, end_pose=end_pose)
	print(f"  Bug2 path length: {len(path2)} steps")

	visualize_bug1_vs_bug2(matrix, path1, path2, start_pose, end_pose)
