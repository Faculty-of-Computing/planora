# 📝 Planor Tasks

---

## 1️⃣ Backend Routes (API Tasks)

### API Endpoints Overview

| **Route**                        | **Method** | **Purpose**             | **Implementation Steps**                         | **👤 Assigned To** | **✅ Done** |
| -------------------------------- | :--------: | ----------------------- | ------------------------------------------------ | :----------------: | :---------: |
| `/api/auth/register`             |    POST    | Create new user         | Validate → Hash password → Save → Return token   |       _Name_       |     ⬜      |
| `/api/auth/login`                |    POST    | Authenticate user       | Validate → Compare password → Return JWT         |       _Name_       |     ⬜      |
| `/api/auth/logout`               |    POST    | Logout user             | Invalidate session/cookie                        |       _Name_       |     ⬜      |
| `/api/auth/me`                   |    GET     | Get current user        | JWT middleware → Fetch user                      |       _Name_       |     ⬜      |
| `/api/events`                    |    GET     | List all events         | Query DB → Filters → Return list                 |       _Name_       |     ⬜      |
| `/api/events`                    |    POST    | Create new event        | Auth → Validate → Save event with `creatorId`    |       _Name_       |     ⬜      |
| `/api/events/:eventId`           |    GET     | Event details           | Fetch from DB → Include tickets, attendees count |       _Name_       |     ⬜      |
| `/api/events/:eventId`           |    PUT     | Update event            | Auth → Verify ownership → Update fields          |       _Name_       |     ⬜      |
| `/api/events/:eventId`           |   DELETE   | Delete event            | Auth → Verify ownership → Soft/hard delete       |       _Name_       |     ⬜      |
| `/api/events/:eventId/register`  |    POST    | Register user for event | Auth → Check already registered → Add record     |       _Name_       |     ⬜      |
| `/api/events/:eventId/attendees` |    GET     | View attendees          | Auth → Verify owner → Fetch attendees            |       _Name_       |     ⬜      |
| `/api/events/:eventId/tickets`   |    GET     | Ticket options          | Fetch ticket tiers from DB                       |       _Name_       |     ⬜      |
| `/api/events/:eventId/tickets`   |    POST    | Buy ticket              | Auth → Payment → Save purchase                   |       _Name_       |     ⬜      |
| `/api/tickets/:ticketId`         |    GET     | View ticket             | Auth → Verify owner → Return ticket/QR           |       _Name_       |     ⬜      |

---

## 2️⃣ Frontend Routes (UI Tasks)

### UI Pages Overview

| **Route**                    | **Purpose**               | **Implementation Steps**                                         | **👤 Assigned To** | **✅ Done** |
| ---------------------------- | ------------------------- | ---------------------------------------------------------------- | :----------------: | :---------: |
| `/`                          | Homepage (events list)    | Fetch `/api/events` → Display cards with ticket availability     |       _Name_       |     ⬜      |
| `/login`                     | Login page                | Form → POST `/api/auth/login` → Store token → Redirect           |       _Name_       |     ⬜      |
| `/register`                  | Registration page         | Form → POST `/api/auth/register` → Auto-login                    |       _Name_       |     ⬜      |
| `/events`                    | Browse events             | Fetch `/api/events` → Filters/search                             |       _Name_       |     ⬜      |
| `/events/create`             | Create event              | Form → POST `/api/events`                                        |       _Name_       |     ⬜      |
| `/events/:eventId`           | Event details (shareable) | GET `/api/events/:eventId` → Show info, register, buy tickets    |       _Name_       |     ⬜      |
| `/events/:eventId/edit`      | Edit event                | Auth → Verify owner → PUT `/api/events/:eventId`                 |       _Name_       |     ⬜      |
| `/events/:eventId/attendees` | Attendees list            | Auth → Verify owner → GET `/api/events/:eventId/attendees`       |       _Name_       |     ⬜      |
| `/tickets/:ticketId`         | Ticket view               | GET `/api/tickets/:ticketId` → Show QR                           |       _Name_       |     ⬜      |
| `/profile`                   | User profile              | GET `/api/auth/me` → Show created events, registrations, tickets |       _Name_       |     ⬜      |
