# Interview Preparation Guide - Green Event Platform
# 面试准备指南 - 绿色活动平台

---

## 1. SYSTEM INTRODUCTION / 系统介绍

### English Version:
"Good morning/afternoon. We're presenting the **Green Event Platform**, a community-driven web application built with Flask that connects volunteers and organizers for environmental activities.

**Core Purpose**: The platform enables organizers to create and manage green events (like beach cleanups, tree planting, recycling workshops), while volunteers can discover events, join them, track their participation hours, and provide feedback.

**Key Features**:
- **Multi-role System**: Three user types - Volunteers, Organizers, and Admins, each with different permissions
- **Event Management**: Organizers create events; volunteers join and track hours
- **Leaderboard**: Ranks volunteers by total participation hours
- **Visitor Mode**: Non-logged-in users can browse events without registration
- **Admin Dashboard**: Complete system management including user banning, role changes, and log viewing
- **Customization**: Light/dark theme toggle and custom background images
- **Security**: Password encryption, comprehensive data validation, and role-based access control"

### 中文版本：
"早上好/下午好。我们展示的是**绿色活动平台**，一个基于Flask构建的社区驱动型Web应用，连接志愿者和组织者进行环保活动。

**核心目的**：平台让组织者创建和管理绿色活动（如海滩清理、植树、回收工作坊），志愿者可以发现活动、参与、追踪参与时长并提供反馈。

**主要功能**：
- **多角色系统**：三种用户类型 - 志愿者、组织者和管理员，各自拥有不同权限
- **活动管理**：组织者创建活动；志愿者加入并追踪时长
- **排行榜**：按总参与时长对志愿者进行排名
- **访客模式**：未登录用户可浏览活动而无需注册
- **管理员面板**：完整的系统管理，包括用户封禁、角色更改和日志查看
- **个性化**：明暗主题切换和自定义背景图片
- **安全性**：密码加密、全面的数据验证和基于角色的访问控制"

---

## 2. CODE STRUCTURE & FILE LOCATIONS / 代码结构与文件位置

### Core Files / 核心文件：

| File / 文件 | Purpose / 用途 | Key Functions / 关键功能 |
|------------|---------------|------------------------|
| `blogapp/models.py` | Database models / 数据库模型 | User, Event, Participation, Feedback models |
| `blogapp/routes.py` | All routes & business logic / 所有路由和业务逻辑 | CRUD operations, authentication, authorization |
| `blogapp/forms.py` | WTForms definitions / WTForms定义 | Form validation classes |
| `blogapp/config.py` | Configuration / 配置 | Environment variables, database URI, logging setup |
| `blogapp/__init__.py` | App initialization / 应用初始化 | Flask app setup, database, logging handlers |
| `blogapp/templates/` | HTML templates / HTML模板 | Jinja2 templates for all pages |
| `blogapp/static/js/` | JavaScript files / JavaScript文件 | Theme switching, form validation, AJAX |
| `blogapp/static/style/` | CSS files / CSS文件 | Styling, theme variables |

---

## 3. CRUD OPERATIONS - WHERE TO FIND THEM / 增删改查操作 - 在哪里找

### CREATE (添加) / 创建操作：

**Location / 位置**: `blogapp/routes.py`

| Feature / 功能 | Route / 路由 | Function Name / 函数名 | Lines |
|---------------|-------------|----------------------|-------|
| Create User / 创建用户 | `/signup` | `signup()` | ~181-222 |
| Create Event / 创建活动 | `/create_event` | `create_event()` | ~518-537 |
| Join Event / 加入活动 | `/join_event/<id>` | `join_event()` | ~395-419 |
| Submit Feedback / 提交反馈 | `/feedback/<id>` | `feedback()` | ~469-480 |
| Upload Avatar / 上传头像 | `/edit_profile` | `edit_profile()` | ~321-333 |

**Key Code Pattern / 关键代码模式**:
```python
new_item = Model(field1=value1, field2=value2)
db.session.add(new_item)
db.session.commit()
```

---

### READ (查询) / 读取操作：

**Location / 位置**: `blogapp/routes.py`

| Feature / 功能 | Route / 路由 | Function Name / 函数名 | Lines |
|---------------|-------------|----------------------|-------|
| View Events / 查看活动 | `/index` | `index()` | ~66-115 |
| View Profile / 查看资料 | `/profile` | `profile()` | ~242-268 |
| View Event Details / 查看活动详情 | `/event/<id>` | `event_detail()` | ~421-467 |
| View Leaderboard / 查看排行榜 | `/leaderboard` | `leaderboard()` | ~482-516 |
| Search Events / 搜索活动 | `/index?search=...` | `index()` | ~73-84 |
| Admin View Users / 管理员查看用户 | `/admin_users` | `admin_users()` | ~746-777 |
| Admin View Logs / 管理员查看日志 | `/admin_logs` | `admin_logs()` | ~980-1091 |

**Key Code Pattern / 关键代码模式**:
```python
# Simple query / 简单查询
items = Model.query.filter_by(field=value).all()

# Search with OR / 带OR的搜索
query = Model.query.filter(
    sa.or_(Model.field1.ilike(f"%{search}%"), 
           Model.field2.ilike(f"%{search}%"))
)

# Join query / 连接查询
results = db.session.query(User.username, 
                           db.func.sum(Participation.hours))
           .join(Participation)
           .group_by(User.id)
           .order_by(...)
```

---

### UPDATE (修改) / 更新操作：

**Location / 位置**: `blogapp/routes.py`

| Feature / 功能 | Route / 路由 | Function Name / 函数名 | Lines |
|---------------|-------------|----------------------|-------|
| Update Profile / 更新资料 | `/edit_profile` | `edit_profile()` | ~269-353 |
| Update Event / 更新活动 | `/event/<id>/edit` | `edit_event()` | ~567-583 |
| Update Event Results / 更新活动结果 | `/event/<id>/results` | `update_results()` | ~691-722 |
| Update User Hours / 更新用户时长 | `/event/<id>/results` | `update_results()` | ~701-709 |
| Admin Update Role / 管理员更新角色 | `/admin_update_role/<id>` | `admin_update_role()` | ~779-804 |
| Admin Update Feedback / 管理员更新反馈 | `/admin_feedback/<id>` | `admin_edit_feedback()` | ~955-969 |
| Ban User / 封禁用户 | `/admin/disable_user/<id>` | `disable_user()` | ~1109-1140 |
| Restore User / 恢复用户 | `/admin/restore_user/<id>` | `restore_user()` | ~1143-1150 |

**Key Code Pattern / 关键代码模式**:
```python
item = Model.query.get_or_404(id)
item.field = new_value
db.session.commit()
```

---

### DELETE (删除) / 删除操作：

**Location / 位置**: `blogapp/routes.py`

| Feature / 功能 | Route / 路由 | Function Name / 函数名 | Lines |
|---------------|-------------|----------------------|-------|
| Delete Account / 删除账户 | `/delete_account` | `delete_account()` | ~355-387 |
| Delete Event / 删除活动 | `/event/<id>/delete` | `delete_event()` | ~586-596 |
| Delete Participant / 删除参与者 | `/event/<id>/manage` | `manage_event()` | ~633-638 |
| Admin Delete User / 管理员删除用户 | `/admin_delete_user/<id>` | `admin_delete_user()` | ~805-824 |
| Admin Delete Event / 管理员删除活动 | `/admin_delete_event/<id>` | `admin_delete_event()` | ~908-920 |
| Admin Delete Feedback / 管理员删除反馈 | `/admin_feedback/delete/<id>` | `admin_delete_feedback()` | ~971-978 |

**Key Code Pattern / 关键代码模式**:
```python
# Delete single record / 删除单条记录
item = Model.query.get_or_404(id)
db.session.delete(item)
db.session.commit()

# Cascade delete / 级联删除
# Delete related records first / 先删除相关记录
RelatedModel.query.filter_by(foreign_key=id).delete()
Model.query.filter_by(id=id).delete()
db.session.commit()
```

---

## 4. GRADING CRITERIA CHECKLIST / 评分标准检查清单

### ✅ D Grade Requirements / D级要求：

- ✅ **Repository URL & Contribution Statements** / 仓库URL和贡献声明
- ✅ **Attend all meetings** / 参加所有会议
- ✅ **Basic Flask website with login/logout** / 带登录/登出的基础Flask网站
  - Location: `routes.py` - `login()`, `logout()`, `signup()`
- ✅ **Password encryption** / 密码加密
  - Location: `routes.py` - Uses `generate_password_hash()` and `check_password_hash()`
  - Code: Line ~135, ~208

---

### ✅ C Grade Requirements / C级要求：

- ✅ **Data validation beyond slides/labs** / 超出幻灯片/实验的数据验证
  - Location: `forms.py` - All forms have validators
  - Location: `routes.py` - Additional server-side validation (email regex, duplicate checks)
  - Example: `signup()` function validates email format, checks duplicates
- ✅ **Validators for all user-input** / 所有用户输入都有验证器
  - Location: `forms.py` - `DataRequired`, `Email`, `Length`, `EqualTo`, `FileAllowed`
- ✅ **Comments in code** / 代码注释
  - All Python files have English comments
  - JavaScript files have comments (`formGlow.js`, `theme.js`)
  - CSS has section comments
- ✅ **No hard-coded credentials** / 无硬编码凭证
  - Location: `config.py` - Uses `os.environ.get()` for `SECRET_KEY` and `DATABASE_URL`
  - Code: Lines 8, 10-11

---

### ✅ B Grade Requirements / B级要求：

- ✅ **AJAX page updates (more than one page)** / AJAX页面更新（多个页面）
  - **Signup Page** / 注册页面:
    - Location: `templates/signup.html` - Lines 127-136
    - Real-time username/email duplicate checking via `/check_username` and `/check_email`
    - Routes: `routes.py` - Lines 225-240
  - **Form Validation** / 表单验证:
    - Location: `static/js/formGlow.js` - Real-time input validation with visual feedback
- ✅ **Visitor mode navigation** / 访客模式导航
  - Location: `routes.py` - `visitor_entry()` - Line 55
  - Visitors can view events, leaderboard without login
  - Template: `templates/visitor_index.html`
- ✅ **Different user types interact** / 不同用户类型交互
  - Volunteers join events created by Organizers
  - Organizers manage participants and view feedback from Volunteers
  - Admins can manage all users and events
- ✅ **JavaScript changes CSS based on user interaction** / JavaScript根据用户交互改变CSS
  - Location: `static/js/formGlow.js`
  - Adds/removes `input-valid` and `input-error` classes dynamically
  - CSS classes defined in `static/style/mystyle.css` - Lines 422-444
- ✅ **Delete account functionality** / 删除账户功能
  - Location: `routes.py` - `delete_account()` - Lines 355-387
  - Template: `templates/profile.html` - Delete button with confirmation
  - Deletes user and all related data (participations, feedbacks, events)

---

### ✅ A Grade Requirements / A级要求：

- ✅ **Aesthetically pleasing styling** / 美观的样式
  - Location: `static/style/mystyle.css`
  - Consistent color scheme, card-based layout, responsive design
  - Dark theme support with CSS variables
- ✅ **No dead links or broken functions** / 无死链接或损坏功能
  - All routes tested and working
  - Navigation links properly configured
- ✅ **User customization UI** / 用户自定义UI
  - **Light/Dark Mode** / 明暗模式:
    - Location: `static/js/theme.js` - `toggleTheme()`
    - Toggles `dark-theme` class on body
    - Saved in localStorage
  - **Custom Background** / 自定义背景:
    - Location: `static/js/theme.js` - `uploadCustomBackground()`
    - Users can upload background images
    - Stored in localStorage as data URL
- ✅ **Admin user functionality** / 管理员用户功能
  - **Edit/Delete Users** / 编辑/删除用户:
    - Routes: `/admin_users`, `/admin_delete_user/<id>`, `/admin_update_role/<id>`
  - **Ban Users** / 封禁用户:
    - Route: `/admin/disable_user/<id>` - Lines 1109-1140
    - Supports temporary and permanent bans
    - Shows ban reason and remaining time on login attempt
  - **Edit/Delete Events** / 编辑/删除活动:
    - Routes: `/admin_events`, `/admin_event/<id>`, `/admin_delete_event/<id>`
  - **Edit/Delete Feedback** / 编辑/删除反馈:
    - Routes: `/admin_feedback`, `/admin_feedback/<id>`, `/admin_feedback/delete/<id>`
- ✅ **Log file system** / 日志文件系统
  - **Logging Setup** / 日志设置:
    - Location: `__init__.py` - Lines 18-46
    - Uses `RotatingFileHandler` for log rotation
    - Logs to `logs/app.log`
  - **Log Viewing** / 日志查看:
    - Route: `/admin_logs` - Lines 980-1091
    - Admin-only access
    - Filter by level (INFO, WARNING, ERROR)
    - Search by keyword
    - Pagination support
  - **Log Usage** / 日志使用:
    - Login attempts logged: `app.logger.warning()` - Line 130, 136, 149
    - Successful login: `app.logger.info()` - Line 171
    - Auto-unban: `app.logger.info()` - Line 161
- ✅ **Extra creative functionality** / 额外创意功能
  - **Temporary Ban System** / 临时封禁系统:
    - Location: `models.py` - User model properties:
      - `is_currently_banned` - Line 32-46
      - `ban_remaining_time` - Line 48-77
      - `unban()` method - Line 79-83
    - Location: `routes.py`:
      - Ban check on login - Lines 144-162
      - Auto-unban when ban expires
      - Shows ban status, reason, and remaining time
    - **Features** / 功能:
      - Permanent bans (no end time)
      - Temporary bans (with expiration)
      - Automatic unban when time expires
      - Ban reason tracking
      - User-friendly time remaining display

---

## 5. HIGHLIGHT FEATURES TO MENTION / 需要强调的亮点功能

### Must Mention / 必须提及：

1. **Temporary Ban System with Auto-Unban** / 带自动解封的临时封禁系统
   - **Why it's special** / 为什么特别:
     - Not just a simple ban/unban - includes time-based expiration
     - Automatically checks and unbans users when ban period expires
     - User-friendly display of remaining ban time (days, hours, minutes)
   - **Where to show** / 在哪里展示:
     - Admin panel: Ban a user with time limit
     - Try to login as banned user: Shows ban reason and time remaining
     - After ban expires: User can login automatically

2. **Comprehensive Logging System** / 全面的日志系统
   - **Why it's special** / 为什么特别:
     - Rotating file handler prevents log files from growing too large
     - Admin can filter by level (INFO, WARNING, ERROR)
     - Keyword search functionality
     - Pagination for large log files
   - **Where to show** / 在哪里展示:
     - Admin dashboard → System Logs
     - Show filtering by level
     - Show search functionality

3. **Real-time AJAX Validation** / 实时AJAX验证
   - **Why it's special** / 为什么特别:
     - Username and email duplicate checking happens as user types
     - No page refresh needed
     - Visual feedback with CSS class changes
   - **Where to show** / 在哪里展示:
     - Signup page: Type a username that exists → instant error
     - Form fields change color (green for valid, red for error)

4. **Visitor Mode** / 访客模式
   - **Why it's special** / 为什么特别:
     - Allows non-registered users to explore the platform
     - Can view events and leaderboard
     - Encourages signup without forcing registration
   - **Where to show** / 在哪里展示:
     - Welcome page → "Continue as Visitor"
     - Show that visitors can browse but cannot join events

5. **JavaScript Dynamic CSS Styling** / JavaScript动态CSS样式
   - **Why it's special** / 为什么特别:
     - Form validation adds/removes CSS classes in real-time
     - Visual feedback (green glow for valid, red shake for invalid)
     - CSS classes defined in stylesheet, applied by JavaScript
   - **Where to show** / 在哪里展示:
     - Any form page: Type invalid input → see red border and shake
     - Type valid input → see green border

---

## 6. COMMON QUESTIONS & ANSWERS / 常见问题与答案

### Q1: "How does user authentication work?" / "用户认证如何工作？"

**Answer / 答案**:
- Location: `routes.py` - `login()` function (Lines 117-179)
- Uses `werkzeug.security.check_password_hash()` to verify passwords
- Passwords stored as hashes using `generate_password_hash()` during signup
- Session stores: `USERNAME`, `USER_ID`, `ROLE`
- Decorator `@login_required()` protects routes (Lines 17-41)

---

### Q2: "How do you prevent duplicate usernames/emails?" / "如何防止重复用户名/邮箱？"

**Answer / 答案**:
- **Server-side** / 服务器端:
  - Location: `routes.py` - `signup()` function
  - Checks database before creating user (Lines 198-205)
- **Client-side (AJAX)** / 客户端（AJAX）:
  - Location: `templates/signup.html` - Lines 127-136
  - Real-time checking via `/check_username` and `/check_email` endpoints
  - Routes: `routes.py` - Lines 225-240
  - Shows error immediately as user types

---

### Q3: "How does the ban system work?" / "封禁系统如何工作？"

**Answer / 答案**:
- **Model Properties** / 模型属性:
  - Location: `models.py` - User model
  - `is_currently_banned` property (Lines 32-46): Checks if ban is active
  - `ban_remaining_time` property (Lines 48-77): Calculates time left
- **Ban Logic** / 封禁逻辑:
  - Location: `routes.py` - `disable_user()` (Lines 1109-1140)
  - Sets `is_disabled=True`, `disabled_until` (datetime or None), `disabled_reason`
- **Login Check** / 登录检查:
  - Location: `routes.py` - `login()` function (Lines 144-162)
  - Checks `is_currently_banned` before allowing login
  - Shows ban reason and remaining time
  - Auto-unbans if ban period expired

---

### Q4: "How does AJAX work in your project?" / "AJAX在你的项目中如何工作？"

**Answer / 答案**:
- **Signup Page** / 注册页面:
  - Location: `templates/signup.html` - Lines 127-136
  - Uses `fetch()` API to call `/check_username` and `/check_email`
  - Backend returns JSON: `jsonify({'exists': True/False})`
  - Updates UI without page refresh
- **Backend Endpoints** / 后端端点:
  - Location: `routes.py` - Lines 225-240
  - Returns JSON responses using `jsonify()`

---

### Q5: "How does JavaScript change CSS?" / "JavaScript如何改变CSS？"

**Answer / 答案**:
- **Form Validation** / 表单验证:
  - Location: `static/js/formGlow.js`
  - Adds/removes classes: `input-valid` and `input-error`
  - CSS classes defined in `static/style/mystyle.css` (Lines 422-444)
  - Classes applied based on validation results
- **Theme Toggle** / 主题切换:
  - Location: `static/js/theme.js` - `toggleTheme()`
  - Adds/removes `dark-theme` class on `<body>`
  - CSS uses `body.dark-theme` selector to apply dark styles

---

### Q6: "Where is data validation done?" / "数据验证在哪里完成？"

**Answer / 答案**:
- **Client-side** / 客户端:
  - Location: `templates/signup.html` - JavaScript validation
  - Location: `static/js/formGlow.js` - Real-time visual feedback
- **Server-side (WTForms)** / 服务器端（WTForms）:
  - Location: `forms.py` - All forms have validators
  - Examples: `DataRequired`, `Email`, `Length`, `EqualTo`
- **Server-side (Custom)** / 服务器端（自定义）:
  - Location: `routes.py` - `signup()` function
  - Email regex validation (Line 192)
  - Duplicate checks (Lines 198-205)
  - File type validation for uploads (Lines 326, 340)

---

### Q7: "How does the logging system work?" / "日志系统如何工作？"

**Answer / 答案**:
- **Setup** / 设置:
  - Location: `__init__.py` - Lines 18-46
  - Uses Python `logging` module with `RotatingFileHandler`
  - Logs to `logs/app.log` with rotation (10KB max, 10 backups)
- **Usage** / 使用:
  - Location: `routes.py` - Various functions
  - `app.logger.info()` for successful operations
  - `app.logger.warning()` for failed login attempts
  - `app.logger.error()` for errors
- **Viewing** / 查看:
  - Location: `routes.py` - `admin_logs()` (Lines 980-1091)
  - Admin-only route
  - Filters by level, searches by keyword, pagination

---

### Q8: "How do different user roles interact?" / "不同用户角色如何交互？"

**Answer / 答案**:
- **Volunteer → Organizer** / 志愿者 → 组织者:
  - Volunteers join events created by Organizers
  - Volunteers submit feedback on events
  - Organizers view feedback and manage participants
- **Admin → All Users** / 管理员 → 所有用户:
  - Admins can view/edit/delete any user
  - Admins can view/edit/delete any event
  - Admins can ban/unban users
  - Admins can change user roles
- **Implementation** / 实现:
  - Location: `routes.py` - `login_required(role=...)` decorator
  - Role-based access control (Lines 17-41)

---

## 7. DEMONSTRATION FLOW / 演示流程建议

### Suggested Order / 建议顺序：

1. **Welcome Page** / 欢迎页面
   - Show visitor mode option
   - Explain public access

2. **Signup Process** / 注册流程
   - Show real-time AJAX validation
   - Show form validation with CSS changes
   - Create a test user

3. **Login** / 登录
   - Show password encryption (mention it)
   - Show session management

4. **Event Management** / 活动管理
   - Create an event (as Organizer)
   - Join an event (as Volunteer)
   - Show search functionality

5. **Profile & Customization** / 资料和自定义
   - Show profile page
   - Show theme toggle (light/dark)
   - Show custom background upload
   - Show delete account option

6. **Admin Features** / 管理员功能
   - Show admin dashboard
   - Demonstrate ban system (temporary ban)
   - Show log viewing with filters
   - Show user/event management

7. **Leaderboard** / 排行榜
   - Show volunteer rankings
   - Explain how hours are calculated

8. **Visitor Mode** / 访客模式
   - Switch to visitor
   - Show what visitors can/cannot do

---

## 8. QUICK REFERENCE - FILE LOCATIONS / 快速参考 - 文件位置

### When Asked "Where is X?" / 当被问到"X在哪里？"

| Feature / 功能 | File / 文件 | Function/Class / 函数/类 |
|--------------|------------|------------------------|
| User login / 用户登录 | `routes.py` | `login()` |
| User signup / 用户注册 | `routes.py` | `signup()` |
| Create event / 创建活动 | `routes.py` | `create_event()` |
| Delete event / 删除活动 | `routes.py` | `delete_event()` |
| Update profile / 更新资料 | `routes.py` | `edit_profile()` |
| Ban user / 封禁用户 | `routes.py` | `disable_user()` |
| View logs / 查看日志 | `routes.py` | `admin_logs()` |
| Database models / 数据库模型 | `models.py` | `User`, `Event`, `Participation`, `Feedback` |
| Form validation / 表单验证 | `forms.py` | All form classes |
| AJAX duplicate check / AJAX重复检查 | `routes.py` | `check_username()`, `check_email()` |
| JavaScript form validation / JavaScript表单验证 | `static/js/formGlow.js` | Form validation logic |
| Theme switching / 主题切换 | `static/js/theme.js` | `ThemeManager` class |
| CSS styling / CSS样式 | `static/style/mystyle.css` | All styles |
| Logging setup / 日志设置 | `__init__.py` | Logging configuration |
| Environment variables / 环境变量 | `config.py` | `Config` class |

---

## 9. KEY CODE SNIPPETS TO REMEMBER / 需要记住的关键代码片段

### Password Hashing / 密码哈希：
```python
# Signup / 注册
password_hash = generate_password_hash(password)

# Login / 登录
if check_password_hash(user.password_hash, password):
    # Success
```

### Database Query Patterns / 数据库查询模式：
```python
# Get all / 获取所有
items = Model.query.all()

# Filter / 过滤
items = Model.query.filter_by(field=value).all()

# Search / 搜索
query = Model.query.filter(Model.field.ilike(f"%{search}%"))

# Join / 连接
results = db.session.query(User, Event).join(Event).all()
```

### AJAX Endpoint / AJAX端点：
```python
@app.route('/endpoint', methods=['POST'])
def endpoint():
    data = request.get_json()
    # Process data
    return jsonify({'result': value})
```

### JavaScript AJAX Call / JavaScript AJAX调用：
```javascript
const res = await fetch('/endpoint', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ key: value })
});
const data = await res.json();
```

---

## 10. FINAL TIPS / 最后提示

1. **Be Confident** / 保持自信:
   - You know your code - you built it!
   - If you don't remember exact line numbers, that's okay - describe the function/file

2. **Show, Don't Just Tell** / 展示，不只是说:
   - Actually demonstrate features
   - Let the professor test the website
   - Point out features they might miss

3. **Explain the "Why"** / 解释"为什么":
   - Why did you choose this approach?
   - Why is this feature useful?
   - What problem does it solve?

4. **Be Ready for Code Questions** / 准备好代码问题:
   - They might ask you to find specific code
   - Know your file structure
   - Know your main functions

5. **Highlight Your Extra Features** / 突出你的额外功能:
   - Temporary ban system is your creative feature
   - Make sure to demonstrate it fully
   - Explain how it's better than simple ban/unban

---

**Good luck with your interview! / 祝面试顺利！** 🍀

