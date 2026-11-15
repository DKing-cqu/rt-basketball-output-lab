# 篮球追踪输出练习

对应《技术选型与原型》任务二。项目逐帧检测橙色篮球，生成带标记的视频和逐帧 CSV。你需要在这个基础上增加关键帧截图。

## 运行

在 Ubuntu 或 WSL 的仓库根目录执行以下命令。使用 Python 3.10–3.13。

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m basketball --demo --output-dir runs/baseline
```

`--demo` 会生成一段合成视频，用来检查安装、读取和输出。正式验收统一使用[飞书培训文档中任务二的实拍视频](https://gcnhkq914dqv.feishu.cn/wiki/FRLKwEGQmiAteqkJHLUc8nU2ncd#doxcnpqrTZQIZU7CzLTJQpk3Ypg)。下载为 `samples/basketball.mp4` 后运行：

```bash
python -m basketball --input samples/basketball.mp4 --output-dir runs/baseline
```

路径可以替换成你保存视频的实际位置。复测时使用同一段视频，并把改动后的输出写到另一个目录，方便和基线对照。

- `tracking.csv` 每帧一行，含帧号、时间、追踪状态和位置。帧号从 0 开始；未检测到时状态为 `lost`，坐标留空。
- `annotated.mp4` 画出已检测到的篮球并标明当前帧号及状态。
- 合成视频共 96 帧，0–31 帧可见，32–63 帧遮挡，64–95 帧重新出现。这些帧段仅适用于合成视频。

## 模块

| 模块 | 职责 |
| --- | --- |
| `video.py` | 读取视频帧及初始化视频写入器 |
| `detection.py` | 从单帧定位篮球并返回坐标和半径 |
| `tracking.py` | 将单帧检测整理为带帧号、时间和状态的结果 |
| `output.py` | 用结果绘制标注并写出 CSV 和视频 |
| `__main__.py` | 解析参数和串联处理流程 |
| `demo.py` | 生成合成视频 |

在自己的仓库分支完成改动。保留原有视频和 CSV，复用已有检测结果，并输出正常可见、完全出画和重新进入画面三个阶段的截图。按飞书文档的任务二要求提交分支链接、截图和复测记录。
