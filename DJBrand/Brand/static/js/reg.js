document.addEventListener('DOMContentLoaded', function () {
  const passwordInput = document.getElementById('id_password1');
  const togglePasswordButton = document.getElementById('toggle-password');
  const form = document.getElementById('add_form');
  const successMessage = document.getElementById('success-message');  // Додано посилання на блок повідомлення

  togglePasswordButton.addEventListener('click', function () {
    if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      togglePasswordButton.textContent = '🙈';
    }
    else {
      passwordInput.type = 'password';
      togglePasswordButton.textContent = '🐵';
    }
    formContainer.style.display = 'none';
    successMessage.style.display = 'block';  // Показати блок повідомлення
    form.reset();
  });
});
