# 📝 Planora Tasks

---

## 1️⃣ Backend Routes (API Tasks)

### API Endpoints Overview

| **Route**                        | **Method** | **Purpose**             | **Implementation Steps**                                   | **👤 Assigned To** | **✅ Done** |
| -------------------------------- | :--------: | ----------------------- | ---------------------------------------------------------- | :----------------: | :---------: |
| `/api/auth/register`             |    POST    | Create new user         | Validate → Store password → Save → Store user id as cookie |      Emediong      |     ✅      |
| `/api/auth/login`                |    POST    | Authenticate user       | Validate → Compare password → Store user id as cookie      |      Emediong      |     ✅      |
| `/api/auth/logout`               |    POST    | Logout user             | Remove user id cookie                                      |      Emediong      |     ✅      |
| `/api/auth/me`                   |    GET     | Get current user        | Auth → Fetch user                                          |      Emediong      |     ✅      |
| `/api/events`                    |    GET     | List all events         | Query DB → Filters → Return list                           |     Idaraobong     |     ✅      |
| `/api/events`                    |    POST    | Create new event        | Auth → Validate → Save event with `creatorId`              |     Idaraobong     |     ✅      |
| `/api/events/:eventId`           |    GET     | Event details           | Fetch from DB → Include tickets, attendees count           |     Idaraobong     |     ✅      |
| `/api/events/:eventId`           |    PUT     | Update event            | Auth → Verify ownership → Update fields                    |     Idaraobong     |     ✅      |
| `/api/events/:eventId`           |   DELETE   | Delete event            | Auth → Verify ownership → Soft/hard delete                 |     Idaraobong     |     ✅      |
| `/api/events/:eventId/register`  |    POST    | Register user for event | Auth → Check already registered → Add record               |     Ekomobong      |     ✅      |
| `/api/events/:eventId/attendees` |    GET     | View attendees          | Auth → Verify owner → Fetch attendees                      |       Cravey       |     ⬜      |
| `/api/events/:eventId/tickets`   |    GET     | Ticket options          | Fetch ticket tiers from DB                                 |       Cravey       |     ⬜      |
| `/api/events/:eventId/tickets`   |    POST    | Buy ticket              | Auth → Payment → Save purchase                             |        ---         |     ⬜      |
| `/api/tickets/:ticketId`         |    GET     | View ticket             | Auth → Verify owner → Return ticket/QR                     |       Cravey       |     ⬜      |

---

## 2️⃣ Frontend Routes (UI Tasks)

### UI Pages Overview

| **Route**                    | **Purpose**               | **Implementation Steps**                                         | **👤 Assigned To** | **✅ Done** |
| ---------------------------- | ------------------------- | ---------------------------------------------------------------- | :----------------: | :---------: |
| `/`                          | Homepage (events list)    | Fetch `/api/events` → Display cards with ticket availability     |       Davies       |     ✅      |
| `/login`                     | Login page                | Form → POST `/api/auth/login` → Store token → Redirect           |      Kenneth       |     ✅      |
| `/register`                  | Registration page         | Form → POST `/api/auth/register` → Auto-login                    |      Kenneth       |     ✅      |
| `/events`                    | Browse events             | Fetch `/api/events` → Filters/search                             |       Fidel        |     ⬜      |
| `/events/create`             | Create event              | Form → POST `/api/events`                                        |       Davies       |     ✅      |
| `/events/:eventId`           | Event details (shareable) | GET `/api/events/:eventId` → Show info, register, buy tickets    |       Davies       |     ✅      |
| `/events/:eventId/edit`      | Edit event                | Auth → Verify owner → PUT `/api/events/:eventId`                 |     Daniel Aji     |     ✅      |
| `/events/:eventId/attendees` | Attendees list            | Auth → Verify owner → GET `/api/events/:eventId/attendees`       |     Daniel Aji     |     ✅      |
| `/tickets/:ticketId`         | Ticket view               | GET `/api/tickets/:ticketId` → Show QR                           |       Davies       |     ✅      |
| `/profile`                   | User profile              | GET `/api/auth/me` → Show created events, registrations, tickets |     Daniel Aji     |     ✅      |
