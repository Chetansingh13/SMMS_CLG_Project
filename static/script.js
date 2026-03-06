// Function to simulate downloading a file
function downloadFile(fileName) {
    // In the future, this will link to your backend server
    alert(`Starting download for: ${fileName}`);
}

// Mobile Sidebar Toggle
const menuBtn = document.getElementById('menuBtn');
const sidebar = document.querySelector('.sidebar');

menuBtn.addEventListener('click', () => {
    sidebar.classList.toggle('show');
});

// Simple Search Filter Simulation
const searchInput = document.getElementById('searchInput');
const cards = document.querySelectorAll('.material-card');

searchInput.addEventListener('keyup', function(event) {
    const query = event.target.value.toLowerCase();
    
    cards.forEach(card => {
        const title = card.querySelector('h3').innerText.toLowerCase();
        const description = card.querySelector('p').innerText.toLowerCase();
        
        if(title.includes(query) || description.includes(query)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});