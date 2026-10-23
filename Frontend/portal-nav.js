/**
 * LeadGreen Fellowship — Universal Portal Navigation Controller
 * Provides smooth, accessible mobile off-canvas drawer navigation for all pages using .portal-nav
 */
(function () {
    function initPortalNav() {
        const portalNav = document.querySelector('.portal-nav');
        if (!portalNav) return;

        const navInner = portalNav.querySelector('.nav-inner');
        const navActions = portalNav.querySelector('.nav-actions');
        if (!navInner || !navActions) return;

        // Count navigation links
        const navLinks = navActions.querySelectorAll('.nav-link, .btn-action-primary, .btn-action-outline, .btn-solid-primary');
        
        // If there are 2 or fewer simple links and no special classes, mobile can display them as compact pills
        // But if there are 3+ links, we definitely need the mobile hamburger drawer.
        const needsDrawer = navLinks.length >= 2;

        if (needsDrawer && !navInner.querySelector('.portal-nav-toggle')) {
            // Create hamburger toggle button
            const toggleBtn = document.createElement('button');
            toggleBtn.className = 'portal-nav-toggle';
            toggleBtn.setAttribute('type', 'button');
            toggleBtn.setAttribute('aria-label', 'Toggle navigation menu');
            toggleBtn.setAttribute('aria-expanded', 'false');
            toggleBtn.innerHTML = '<i class="fa-solid fa-bars"></i>';
            navInner.appendChild(toggleBtn);

            // Create backdrop if not already present
            let backdrop = document.querySelector('.portal-nav-backdrop');
            if (!backdrop) {
                backdrop = document.createElement('div');
                backdrop.className = 'portal-nav-backdrop';
                document.body.appendChild(backdrop);
            }

            // Create drawer header if not exists inside navActions
            if (!navActions.querySelector('.nav-drawer-header')) {
                const drawerHeader = document.createElement('div');
                drawerHeader.className = 'nav-drawer-header';
                drawerHeader.innerHTML = `
                    <div class="drawer-brand">
                        <img src="Logo name green.png" alt="LeadGreen Fellowship" onerror="this.src='../Logo name green.png'">
                    </div>
                    <button class="drawer-close-btn" type="button" aria-label="Close navigation menu">
                        <i class="fa-solid fa-xmark"></i>
                    </button>
                `;
                navActions.prepend(drawerHeader);

                const closeBtn = drawerHeader.querySelector('.drawer-close-btn');
                if (closeBtn) {
                    closeBtn.addEventListener('click', closeMenu);
                }
            }

            function openMenu() {
                navActions.classList.add('portal-nav-open');
                backdrop.classList.add('active');
                document.body.classList.add('portal-nav-locked');
                toggleBtn.setAttribute('aria-expanded', 'true');
                const icon = toggleBtn.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-xmark');
                }
            }

            function closeMenu() {
                navActions.classList.remove('portal-nav-open');
                backdrop.classList.remove('active');
                document.body.classList.remove('portal-nav-locked');
                toggleBtn.setAttribute('aria-expanded', 'false');
                const icon = toggleBtn.querySelector('i');
                if (icon) {
                    icon.classList.remove('fa-xmark');
                    icon.classList.add('fa-bars');
                }
            }

            function toggleMenu() {
                if (navActions.classList.contains('portal-nav-open')) {
                    closeMenu();
                } else {
                    openMenu();
                }
            }

            toggleBtn.addEventListener('click', toggleMenu);
            backdrop.addEventListener('click', closeMenu);

            // Close on escape key
            document.addEventListener('keydown', function (e) {
                if (e.key === 'Escape' && navActions.classList.contains('portal-nav-open')) {
                    closeMenu();
                }
            });

            // Close on clicking any link inside drawer on mobile
            navActions.querySelectorAll('.nav-link, a').forEach(function (link) {
                link.addEventListener('click', function () {
                    if (window.innerWidth <= 768) {
                        closeMenu();
                    }
                });
            });
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initPortalNav);
    } else {
        initPortalNav();
    }
})();
