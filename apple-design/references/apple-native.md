# Apple 原生平台参考

实现 SwiftUI、macOS、iOS 或 iPadOS 原生界面时：

- 优先使用原生 SwiftUI 组件、Navigation、Toolbar、Menu、Form、Sheet、Alert 和系统材质。
- 尊重 Safe Area、Dynamic Type、语义系统色、浅色/深色模式和平台输入习惯。
- 不为“更像 Apple”重造已有成熟系统控件。
- iPad/macOS 可利用多列、侧边栏、检查器、快捷键、悬停和上下文菜单；iPhone 优先清晰主列和可触达操作。
- API 是否可用必须按项目 deployment target 核对；涉及新 API 或可能变化的 Apple 平台能力时查阅官方文档。
- 只有部署目标支持时才使用较新的视觉 API；不要虚构 Apple API。
- 平台 HIG 和现有产品交互模式优先于本 skill 中的通用参考数值。
