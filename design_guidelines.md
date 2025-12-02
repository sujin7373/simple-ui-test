# Design Guidelines: React Community Platform

## Design Approach

**Selected Approach:** Hybrid (Reference-Based + Design System)
- **Primary Reference:** Linear's clean aesthetic with Reddit's information density
- **Design System Foundation:** Tailwind utilities with custom component patterns
- **Rationale:** Community platforms require clear information hierarchy and excellent readability while maintaining visual appeal

## Core Design Elements

### Typography
- **Primary Font:** Inter (via Google Fonts CDN)
- **Hierarchy:**
  - H1 (Page Titles): text-3xl md:text-4xl, font-bold
  - H2 (Section Headers): text-2xl md:text-3xl, font-semibold
  - H3 (Card Titles): text-lg md:text-xl, font-semibold
  - Body: text-base, font-normal
  - Small/Meta: text-sm, font-medium
  - Button Text: text-sm md:text-base, font-semibold

### Layout System
**Spacing Units:** Consistent use of 2, 4, 6, 8, 12, and 16
- Component padding: p-4, p-6, p-8
- Section margins: mb-8, mb-12, mb-16
- Card gaps: gap-4, gap-6
- Page containers: max-w-6xl mx-auto px-4

### Component Library

**Navigation Bar:**
- Fixed top position with backdrop blur
- Height: h-16
- Contains: Logo (left), Theme toggle + Auth state (right)
- Login state shows username with dropdown menu
- Logged-out state shows "Sign Up / Login" links

**Authentication Forms (Login/Signup):**
- Centered card design (max-w-md mx-auto)
- Input fields with focus states and clear labels
- Primary CTA button (full width)
- Secondary link for alternate action
- Form validation messages below inputs

**Post Cards:**
- Clean card design with subtle borders
- Structure: Title (bold), Meta info (author, date), Preview text (truncated)
- Hover state with subtle elevation
- Click targets span entire card

**Post List (Landing Page):**
- Vertical stack of 5 recent posts
- Each card: p-6, mb-4, rounded borders
- Empty state message if no posts

**Search Interface:**
- Prominent search input (w-full, max-w-2xl)
- Search icon (Heroicons - MagnifyingGlass)
- Results render below in same card pattern
- Loading state with skeleton cards

**Post Detail Page:**
- Full-width content area (max-w-4xl)
- Title: Large, bold typography
- Meta bar: Author, timestamp, subtle divider
- Content: Generous line-height (leading-relaxed), max-w-prose

**Theme Toggle:**
- Icon-based toggle button (Heroicons - Sun/Moon)
- Smooth transition between states
- Positioned in navbar (top-right)

### Dark/Light Theme Specifications

**Light Theme:**
- Background: Subtle warm gray
- Cards: Pure white with soft shadows
- Text: High contrast dark gray/black
- Borders: Light gray dividers
- Accents: Professional blue/purple tones

**Dark Theme:**
- Background: Deep charcoal/navy
- Cards: Elevated dark surface
- Text: Off-white/light gray
- Borders: Subtle lighter borders
- Accents: Brighter accent colors for visibility

### Interactive States
- **Buttons:** Clear hover (slight opacity/scale), active (pressed feel)
- **Cards:** Hover elevation, smooth transitions
- **Inputs:** Focus rings with theme-appropriate colors
- **Links:** Underline on hover for clarity

### Accessibility
- Clear focus indicators on all interactive elements
- Proper heading hierarchy (h1 → h2 → h3)
- Alt text placeholders for future image content
- ARIA labels for icon-only buttons (theme toggle)

## Page-Specific Layouts

**Signup/Login Pages:**
- Full-height centered layout
- Auth card with logo/title at top
- Form fields with generous spacing (mb-6)
- Error messages in theme-appropriate alert style

**Landing Page (index.html):**
- Welcome header with username greeting
- "Recent Posts" section title
- Post cards in single column (stacked vertically)
- Consistent card styling throughout

**Search Page:**
- Search input prominently positioned at top
- Search button adjacent to input
- Results section below with same post card pattern
- "No results" state with helpful message

**Detail Page:**
- Breadcrumb or back button for navigation
- Post content in reading-optimized width
- Author info card (sidebar or below content)

## Icons
**Library:** Heroicons (via CDN)
**Usage:**
- Search: MagnifyingGlass
- Theme: Sun/Moon
- User: UserCircle
- Logout: ArrowRightOnRectangle
- Back/Navigation: ChevronLeft

## Images
**No hero images required** - This is a utility-focused community platform where content is king. Focus on clean, readable layouts rather than large imagery.

## Animation Guidelines
**Minimal Animations:**
- Theme toggle: 200ms fade transition on body
- Card hover: 150ms elevation change
- Page transitions: None (standard browser navigation)
- Search results: Fade-in (200ms) as they render