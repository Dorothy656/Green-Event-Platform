# Demo Script - Green Event Platform
# 演示脚本 - 绿色活动平台

---

## Opening Statement / 开场白

**English:**
"Good morning/afternoon, Professor [Name] and Quinn. Thank you for this opportunity to present our Green Event Platform. We've built a comprehensive web application using Flask that connects volunteers and organizers for environmental activities. Let me give you a brief overview before we dive into the demonstration."

**中文:**
"早上好/下午好，[教授姓名]和Quinn。感谢这次展示我们绿色活动平台的机会。我们使用Flask构建了一个全面的Web应用，连接志愿者和组织者进行环保活动。在开始演示之前，让我先简要介绍一下。"

---

## System Overview / 系统概述 (30 seconds / 30秒)

**English:**
"Our platform has three main user roles:
- **Volunteers** can discover and join green events, track their participation hours, and provide feedback
- **Organizers** can create and manage events, view participants, and update results
- **Admins** have full system control including user management, event oversight, and log viewing

We also have a **Visitor Mode** that allows non-registered users to browse events without login.

Now, let me show you the key features that meet and exceed the grading criteria."

**中文:**
"我们的平台有三个主要用户角色：
- **志愿者**可以发现和加入绿色活动，追踪参与时长，并提供反馈
- **组织者**可以创建和管理活动，查看参与者，并更新结果
- **管理员**拥有完整的系统控制权，包括用户管理、活动监督和日志查看

我们还有一个**访客模式**，允许未注册用户无需登录即可浏览活动。

现在，让我向您展示满足并超越评分标准的关键功能。"

---

## Feature Demonstrations / 功能演示

### 1. Visitor Mode / 访客模式 (30 seconds)

**English:**
"First, let me show you our Visitor Mode feature. This allows anyone to explore the platform without registration."

*[Navigate to welcome page → Click "Continue as Visitor"]*

"As you can see, visitors can browse all events and view the leaderboard. However, they cannot join events or create them - this encourages signup while still providing value to casual browsers."

**中文:**
"首先，让我展示我们的访客模式功能。这允许任何人在不注册的情况下探索平台。"

*[导航到欢迎页面 → 点击"Continue as Visitor"]*

"如您所见，访客可以浏览所有活动并查看排行榜。但是，他们不能加入活动或创建活动 - 这鼓励注册，同时仍为随意浏览的用户提供价值。"

---

### 2. Real-time AJAX Validation / 实时AJAX验证 (45 seconds)

**English:**
"Now let me demonstrate our real-time validation system. This is one of our AJAX implementations."

*[Go to signup page → Start typing a username that exists]*

"Notice how the system checks for duplicate usernames in real-time as the user types - no page refresh needed. The same happens for email addresses. This provides immediate feedback and improves user experience."

*[Show email validation too]*

**中文:**
"现在让我演示我们的实时验证系统。这是我们的AJAX实现之一。"

*[转到注册页面 → 开始输入已存在的用户名]*

"请注意系统如何在用户输入时实时检查重复用户名 - 无需刷新页面。邮箱地址也是如此。这提供了即时反馈并改善了用户体验。"

*[也展示邮箱验证]*

---

### 3. JavaScript Dynamic CSS Styling / JavaScript动态CSS样式 (30 seconds)

**English:**
"Another feature that meets the grading criteria is JavaScript changing CSS based on user interaction."

*[Fill out form with invalid data]*

"Watch how the input fields change color - red with a shake animation for invalid input, green glow for valid input. The CSS classes are defined in our stylesheet, but JavaScript dynamically adds and removes them based on validation results."

**中文:**
"另一个满足评分标准的功能是JavaScript根据用户交互改变CSS。"

*[填写带有无效数据的表单]*

"请注意输入字段如何改变颜色 - 无效输入为红色并带有抖动动画，有效输入为绿色发光。CSS类在我们的样式表中定义，但JavaScript根据验证结果动态添加和删除它们。"

---

### 4. User Customization / 用户自定义 (45 seconds)

**English:**
"Let me show you our user customization features - this meets the A-grade requirement."

*[Login → Show theme toggle]*

"Users can toggle between light and dark themes. The preference is saved in localStorage."

*[Show custom background upload]*

"Additionally, users can upload custom background images. This is stored in localStorage and persists across sessions."

**中文:**
"让我展示我们的用户自定义功能 - 这满足A级要求。"

*[登录 → 显示主题切换]*

"用户可以在明暗主题之间切换。偏好保存在localStorage中。"

*[显示自定义背景上传]*

"此外，用户可以上传自定义背景图片。这存储在localStorage中，并在会话之间持续存在。"

---

### 5. Admin Features - Ban System / 管理员功能 - 封禁系统 (1 minute)

**English:**
"Now let me demonstrate our creative extra feature - the temporary ban system. This goes beyond simple ban/unban functionality."

*[Login as admin → Go to admin users]*

"Admins can ban users with a specific reason and set an expiration time. Let me ban a test user for 5 minutes."

*[Ban a user with time limit]*

"Now, let me try to login as that banned user."

*[Try to login as banned user]*

"As you can see, the system shows the ban reason and the remaining time. This is much more informative than a simple 'you are banned' message."

*[Wait a moment, then explain auto-unban]*

"Additionally, when the ban period expires, the system automatically unbans the user on their next login attempt. This is handled by the `is_currently_banned` property in our User model, which checks both the disabled status and the expiration time."

**中文:**
"现在让我演示我们的创意额外功能 - 临时封禁系统。这超越了简单的封禁/解封功能。"

*[以管理员身份登录 → 转到管理员用户]*

"管理员可以以特定原因封禁用户并设置过期时间。让我封禁一个测试用户5分钟。"

*[封禁一个带时间限制的用户]*

"现在，让我尝试以该被封禁用户身份登录。"

*[尝试以被封禁用户身份登录]*

"如您所见，系统显示封禁原因和剩余时间。这比简单的'您已被封禁'消息更有信息量。"

*[等待片刻，然后解释自动解封]*

"此外，当封禁期到期时，系统会在用户下次登录尝试时自动解封。这由我们User模型中的`is_currently_banned`属性处理，它检查禁用状态和过期时间。"

---

### 6. Logging System / 日志系统 (45 seconds)

**English:**
"Another A-grade feature is our comprehensive logging system."

*[Go to admin logs]*

"Admins can view all system logs with filtering by level - INFO, WARNING, ERROR. They can also search by keyword."

*[Demonstrate filtering and search]*

"The logs are automatically rotated to prevent files from growing too large. We log important events like login attempts, successful logins, and system errors."

**中文:**
"另一个A级功能是我们全面的日志系统。"

*[转到管理员日志]*

"管理员可以查看所有系统日志，并按级别过滤 - INFO、WARNING、ERROR。他们还可以按关键词搜索。"

*[演示过滤和搜索]*

"日志会自动轮转以防止文件变得过大。我们记录重要事件，如登录尝试、成功登录和系统错误。"

---

### 7. Delete Account / 删除账户 (30 seconds)

**English:**
"Let me show you the delete account functionality, which is a B-grade requirement."

*[Go to profile page]*

"Users can delete their own account. This removes all their data including participations, feedbacks, and if they're an organizer, their events. There's a confirmation dialog to prevent accidental deletion."

**中文:**
"让我展示删除账户功能，这是B级要求。"

*[转到资料页面]*

"用户可以删除自己的账户。这会删除他们的所有数据，包括参与记录、反馈，如果他们是组织者，还包括他们的活动。有一个确认对话框以防止意外删除。"

---

### 8. Event Management / 活动管理 (45 seconds)

**English:**
"Let me demonstrate how different user types interact."

*[Login as organizer → Create an event]*

"Organizers can create events with details like title, description, date, and location."

*[Login as volunteer → Join the event]*

"Volunteers can discover and join events. They can also search for events by title or location."

*[Show search functionality]*

"After events, volunteers can submit feedback, and organizers can update results and manage participants."

**中文:**
"让我演示不同用户类型如何交互。"

*[以组织者身份登录 → 创建活动]*

"组织者可以创建活动，包含标题、描述、日期和地点等详细信息。"

*[以志愿者身份登录 → 加入活动]*

"志愿者可以发现并加入活动。他们还可以按标题或地点搜索活动。"

*[显示搜索功能]*

"活动结束后，志愿者可以提交反馈，组织者可以更新结果并管理参与者。"

---

## Closing Statement / 结束语

**English:**
"To summarize, our platform meets all the grading criteria:

- **D & C**: Basic Flask functionality, password encryption, comprehensive validation, code comments, environment variables
- **B**: AJAX updates on multiple pages, visitor mode, user type interactions, JavaScript CSS changes, delete account
- **A**: Aesthetic styling, no broken links, user customization (theme & background), admin functionality, logging system, and our creative temporary ban system

We're particularly proud of our temporary ban system, which provides a more sophisticated user management solution than simple ban/unban, with automatic expiration and user-friendly feedback.

Thank you for your time. We're happy to answer any questions or demonstrate any specific features in more detail."

**中文:**
"总结一下，我们的平台满足所有评分标准：

- **D & C**: 基础Flask功能、密码加密、全面验证、代码注释、环境变量
- **B**: 多个页面的AJAX更新、访客模式、用户类型交互、JavaScript CSS更改、删除账户
- **A**: 美观的样式、无损坏链接、用户自定义（主题和背景）、管理员功能、日志系统，以及我们创意的临时封禁系统

我们特别为我们的临时封禁系统感到自豪，它提供了比简单封禁/解封更复杂的用户管理解决方案，具有自动过期和用户友好的反馈。

感谢您的时间。我们很乐意回答任何问题或更详细地演示任何特定功能。"

---

## Quick Response Templates / 快速回答模板

### If Asked About Code Location / 如果被问到代码位置：

**English:**
"The [feature] is implemented in `[filename]`, specifically in the `[function_name]()` function around line [number]. Would you like me to show you the code?"

**中文:**
"[功能]在`[文件名]`中实现，具体在`[函数名]()`函数中，大约在第[数字]行。您想让我展示代码吗？"

### If Asked About Implementation Details / 如果被问到实现细节：

**English:**
"We implemented this by [brief explanation]. The key is in [file/function], where we [specific approach]. This allows us to [benefit]."

**中文:**
"我们通过[简要解释]实现了这一点。关键在[文件/函数]中，我们在那里[具体方法]。这使我们能够[好处]。"

### If You Don't Remember Exact Details / 如果您不记得确切细节：

**English:**
"I believe that's in `[filename]`. Let me check the code to give you the exact line number."

**中文:**
"我相信那在`[文件名]`中。让我查看代码以给您确切的行号。"

---

**Remember: Stay calm, be confident, and show your work! / 记住：保持冷静，自信，展示您的工作！** 🍀

