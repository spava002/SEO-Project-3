// Add event listeners to each toggle button
const toggleButtons = document.querySelectorAll('.toggle-btn');
toggleButtons.forEach(button => {
  button.addEventListener('click', () => {
    const content = button.nextElementSibling;
    content.classList.toggle('active');
  });
});