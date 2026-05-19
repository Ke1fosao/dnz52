/* Кастомний JS для сайту ЗДО №52 */

document.addEventListener('DOMContentLoaded', function () {

    /* ---------- Плавний скрол для якірних посилань ---------- */
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            var targetId = this.getAttribute('href');
            if (targetId.length > 1) {
                var target = document.querySelector(targetId);
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        });
    });

    /* ---------- Кнопка "Нагору" ---------- */
    var scrollBtn = document.getElementById('scrollTopBtn');
    if (scrollBtn) {
        var toggleScrollBtn = function () {
            if (window.scrollY > 320) {
                scrollBtn.classList.add('visible');
            } else {
                scrollBtn.classList.remove('visible');
            }
        };
        window.addEventListener('scroll', toggleScrollBtn, { passive: true });
        toggleScrollBtn();

        scrollBtn.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    /* ---------- Активний пункт навігації ---------- */
    var currentPath = window.location.pathname;
    document.querySelectorAll('.navbar .nav-link').forEach(function (link) {
        var href = link.getAttribute('href');
        if (!href || href === '#') return;
        if (currentPath === href || (href !== '/' && currentPath.indexOf(href) === 0)) {
            link.classList.add('active');
        }
    });

    /* ---------- Анімація появи карток на скролі ---------- */
    if ('IntersectionObserver' in window) {
        var fadeEls = document.querySelectorAll('.feature-card, .card, .contact-card');
        var io = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        fadeEls.forEach(function (el) {
            if (!el.classList.contains('no-animate')) {
                el.style.opacity = '0';
                el.style.transform = 'translateY(24px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                io.observe(el);
            }
        });
    }
});
