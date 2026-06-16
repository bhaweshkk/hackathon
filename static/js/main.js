/* ═══════════════════════════════════════════════════════
   HackTeam AI — Main JavaScript
   ═══════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', function () {

  // ── Sidebar mobile toggle ───────────────────────────
  const sidebar   = document.getElementById('sidebar');
  const openBtn   = document.getElementById('sidebarOpen');
  const closeBtn  = document.getElementById('sidebarClose');

  if (openBtn && sidebar) {
    openBtn.addEventListener('click', () => {
      sidebar.classList.add('open');
    });
  }
  if (closeBtn && sidebar) {
    closeBtn.addEventListener('click', () => {
      sidebar.classList.remove('open');
    });
  }
  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', function (e) {
    if (sidebar && sidebar.classList.contains('open')) {
      if (!sidebar.contains(e.target) && e.target !== openBtn) {
        sidebar.classList.remove('open');
      }
    }
  });

  // ── Landing nav scroll accent ───────────────────────
  const landingNav = document.querySelector('.landing-nav');
  if (landingNav) {
    window.addEventListener('scroll', function () {
      landingNav.classList.toggle('scrolled', window.scrollY > 16);
    });
  }

  // ── Auto-dismiss alerts ─────────────────────────────
  document.querySelectorAll('.alert').forEach(function (alert) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
      if (bsAlert) bsAlert.close();
    }, 4000);
  });

  // ── Animate skill bars and score rings on scroll ────
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('animated');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.sb-bar-fill, .ring-fill, .mscore-bar div, .progress-bar-fill').forEach(function (el) {
    observer.observe(el);
  });

  // ── Reveal landing page sections on scroll ───────────
  const revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.16 });

  document.querySelectorAll('.fade-up, .fade-down, .fade-left, .fade-right').forEach(function (el) {
    revealObserver.observe(el);
  });

  // ── Skill row: add / remove ─────────────────────────
  const addSkillBtn = document.getElementById('addSkillBtn');
  if (addSkillBtn) {
    addSkillBtn.addEventListener('click', addSkillRow);
  }

  function addSkillRow() {
    const template = document.querySelector('.skill-template .skill-row');
    if (!template) return;
    const clone = template.cloneNode(true);
    // Clear values
    clone.querySelectorAll('input').forEach(i => i.value = '');
    document.getElementById('skillsContainer').appendChild(clone);
    attachRemove(clone.querySelector('.btn-remove-skill'));
    clone.querySelector('.skill-name-input').focus();
  }

  document.querySelectorAll('.btn-remove-skill').forEach(attachRemove);

  function attachRemove(btn) {
    if (!btn) return;
    btn.addEventListener('click', function () {
      const container = document.getElementById('skillsContainer');
      if (container && container.querySelectorAll('.skill-row').length > 1) {
        this.closest('.skill-row').remove();
      }
    });
  }

  // ── Domain chip toggle ──────────────────────────────
  document.querySelectorAll('.domain-chip input[type=checkbox]').forEach(function (cb) {
    cb.addEventListener('change', function () {
      this.closest('.domain-chip').classList.toggle('selected', this.checked);
    });
  });

  // ── Confirm dangerous actions ───────────────────────
  document.querySelectorAll('[data-confirm]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (!confirm(this.dataset.confirm)) {
        e.preventDefault();
      }
    });
  });

  // ── Bookmark button pulse animation ─────────────────
  document.querySelectorAll('.btn-icon').forEach(function (btn) {
    btn.addEventListener('click', function () {
      this.classList.add('clicked');
      setTimeout(() => this.classList.remove('clicked'), 300);
    });
  });

  // ── Match score ring — animate fill on load ─────────
  document.querySelectorAll('.ring-fill').forEach(function (path) {
    const dashArray = path.getAttribute('stroke-dasharray');
    if (dashArray) {
      path.setAttribute('stroke-dasharray', '0, 100');
      requestAnimationFrame(function () {
        setTimeout(function () {
          path.style.transition = 'stroke-dasharray 1s ease';
          path.setAttribute('stroke-dasharray', dashArray);
        }, 200);
      });
    }
  });

  // ── Progress bars — animate width on load ──────────
  document.querySelectorAll('.progress-bar-fill, .sb-bar-fill, .mscore-bar div').forEach(function (bar) {
    const width = bar.style.width;
    bar.style.width = '0';
    requestAnimationFrame(function () {
      setTimeout(function () {
        bar.style.transition = 'width 0.8s ease';
        bar.style.width = width;
      }, 150);
    });
  });

  // ── Chat: auto-scroll to bottom ─────────────────────
  const chatMessages = document.getElementById('chatMessages');
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Shift+Enter submits, Enter adds newline (if textarea)
    const chatInput = document.querySelector('.chat-input');
    if (chatInput) {
      chatInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.closest('form').submit();
        }
      });
    }
  }

  // ── Tooltip init ────────────────────────────────────
  const tooltipEls = document.querySelectorAll('[title]');
  if (typeof bootstrap !== 'undefined') {
    tooltipEls.forEach(function (el) {
      new bootstrap.Tooltip(el, { trigger: 'hover' });
    });
  }

  // ── Profile form: live character count for bio ──────
  const bioField = document.querySelector('textarea[name=bio]');
  if (bioField) {
    const maxLen = 500;
    const counter = document.createElement('small');
    counter.className = 'text-muted';
    counter.style.float = 'right';
    bioField.parentNode.appendChild(counter);
    function updateCounter() {
      const remaining = maxLen - bioField.value.length;
      counter.textContent = remaining + ' characters remaining';
      counter.style.color = remaining < 50 ? 'var(--danger)' : '';
    }
    bioField.addEventListener('input', updateCounter);
    updateCounter();
  }

  // ── Team size visual indicator ───────────────────────
  document.querySelectorAll('.team-size-badge').forEach(function (badge) {
    const text = badge.textContent.trim(); // e.g. "3/4"
    const parts = text.split('/');
    if (parts.length === 2) {
      const current = parseInt(parts[0]);
      const max     = parseInt(parts[1]);
      if (current >= max) {
        badge.style.background = '#fee2e2';
        badge.style.color = '#991b1b';
      } else if (current >= max - 1) {
        badge.style.background = '#fef3c7';
        badge.style.color = '#92400e';
      }
    }
  });

  // ── Keyboard shortcut: '/' focuses search ───────────
  document.addEventListener('keydown', function (e) {
    if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
      e.preventDefault();
      const searchInput = document.querySelector('.search-input');
      if (searchInput) searchInput.focus();
    }
  });

  // ── Flash effect on page load for active nav item ───
  const activeNav = document.querySelector('.nav-item.active');
  if (activeNav) {
    activeNav.style.transition = 'background 0.5s';
  }

});
