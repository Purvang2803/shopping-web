document.addEventListener('DOMContentLoaded', () => {
  // 🔔 Auto-hide alerts
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => alert.style.opacity = '0', 2500);
    setTimeout(() => alert.style.display = 'none', 3000);
  });

  // 🛒 Quantity input safety
  document.querySelectorAll('input[name="quantity"]').forEach(input => {
    input.addEventListener('input', () => {
      input.value = Math.max(1, parseInt(input.value) || 1);
    });
  });

  // ❌ Confirm before delete
  document.querySelectorAll('.btn-danger').forEach(btn => {
    btn.addEventListener('click', e => {
      if (!confirm("Remove this item from your cart?")) e.preventDefault();
    });
  });

  // 📱 Collapse navbar on link click
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  const navbar = document.querySelector('.navbar-collapse');
  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (navbar.classList.contains('show')) {
        $('.navbar-collapse').collapse('hide');
      }
    });
  });

  // 👁 Toggle password visibility
  document.querySelectorAll('input[type="password"]').forEach(input => {
    const toggle = document.createElement('span');
    toggle.innerHTML = '👁️';
    toggle.style.cursor = 'pointer';
    toggle.style.marginLeft = '10px';
    toggle.style.userSelect = 'none';
    toggle.title = "Show/Hide Password";
    input.parentNode.style.display = 'flex';
    input.parentNode.style.alignItems = 'center';
    input.parentNode.appendChild(toggle);

    toggle.addEventListener('click', () => {
      input.type = input.type === 'password' ? 'text' : 'password';
    });
  });

  // 🌍 Dynamic city dropdown
  const stateSelect = document.getElementById('id_state');
  const citySelect = document.getElementById('id_city');
  const cities = {
    Gujarat: ['Ahmedabad', 'Surat', 'Rajkot', 'Vadodara'],
    Maharashtra: ['Mumbai', 'Pune', 'Nagpur'],
    Rajasthan: ['Jaipur', 'Udaipur', 'Jodhpur'],
    TamilNadu: ['Chennai', 'Madurai', 'Coimbatore'],
    Kerala: ['Kochi', 'Kozhikode', 'Trivandrum']
  };

  if (stateSelect && citySelect) {
    stateSelect.addEventListener('change', () => {
      const selected = stateSelect.value;
      citySelect.innerHTML = '<option value="">Select City</option>';
      (cities[selected] || []).forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        citySelect.appendChild(option);
      });
    });
  }

  // 💦 Ripple effect on buttons
  document.querySelectorAll('button').forEach(btn => {
    btn.style.position = 'relative';
    btn.style.overflow = 'hidden';
    btn.addEventListener('click', e => {
      const ripple = document.createElement('span');
      ripple.className = 'ripple';
      ripple.style.left = `${e.offsetX}px`;
      ripple.style.top = `${e.offsetY}px`;
      btn.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    });
  });

  // 🔥 Toast messages
  window.showToast = (msg = "Success!", type = "success") => {
    const toast = document.createElement('div');
    toast.className = `custom-toast ${type}`;
    toast.innerText = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 4000);
  };

});
