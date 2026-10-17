/**
 * LeadGreen Admin - Responsive Navigation Controller
 * Adds mobile topbar and toggles off-canvas drawer navigation for tablets and mobile devices.
 */
document.addEventListener('DOMContentLoaded', function () {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return; // Not an admin page with a sidebar (e.g., login page)

    // Check if mobile topbar already exists
    if (!document.querySelector('.admin-mobile-topbar')) {
        const topbar = document.createElement('header');
        topbar.className = 'admin-mobile-topbar';
        topbar.innerHTML = `
            <div class="topbar-brand">
                <a href="index.html">
                    <img src="Logo name green.png" alt="LeadGreen Admin" onerror="this.src='../Logo name green.png'">
                </a>
            </div>
            <button class="admin-menu-btn" id="adminSidebarToggle" aria-label="Toggle navigation menu">
                <i class="fa-solid fa-bars"></i>
            </button>
        `;
        document.body.prepend(topbar);
    }

    // Check if backdrop overlay already exists
    let backdrop = document.getElementById('adminSidebarBackdrop');
    if (!backdrop) {
        backdrop = document.createElement('div');
        backdrop.className = 'admin-sidebar-backdrop';
        backdrop.id = 'adminSidebarBackdrop';
        document.body.appendChild(backdrop);
    }

    const toggleBtn = document.getElementById('adminSidebarToggle');

    function openSidebar() {
        sidebar.classList.add('active');
        backdrop.classList.add('active');
        document.body.classList.add('admin-sidebar-open');
        if (toggleBtn) {
            const icon = toggleBtn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-xmark');
            }
        }
    }

    function closeSidebar() {
        sidebar.classList.remove('active');
        backdrop.classList.remove('active');
        document.body.classList.remove('admin-sidebar-open');
        if (toggleBtn) {
            const icon = toggleBtn.querySelector('i');
            if (icon) {
                icon.classList.remove('fa-xmark');
                icon.classList.add('fa-bars');
            }
        }
    }

    function toggleSidebar() {
        if (sidebar.classList.contains('active')) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }

    if (toggleBtn) {
        toggleBtn.addEventListener('click', toggleSidebar);
    }

    backdrop.addEventListener('click', closeSidebar);

    // Auto-close drawer on pressing Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && sidebar.classList.contains('active')) {
            closeSidebar();
        }
    });

    // Auto-close drawer when clicking on any navigation item on mobile
    sidebar.querySelectorAll('.nav-item').forEach(function (navItem) {
        navItem.addEventListener('click', function () {
            if (window.innerWidth <= 992) {
                closeSidebar();
            }
        });
    });
});
