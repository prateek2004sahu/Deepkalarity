const API_BASE = "http://127.0.0.1:8000/api";

function switchTab(tabId) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
    // Remove active class from buttons
    document.querySelectorAll('.tabs button').forEach(el => el.classList.remove('active'));
    
    // Show selected tab and make button active
    document.getElementById(tabId).classList.remove('hidden');
    document.getElementById(tabId + '-btn').classList.add('active');
    
    // Load history if switching to Tab 2
    if(tabId === 'tab2') loadHistory();
}

async function extractRecipe() {
    const url = document.getElementById('url-input').value;
    if(!url) return alert("Please enter a URL or 'test_recipe'");
    
    // Show loader, hide results
    document.getElementById('loader').classList.remove('hidden');
    document.getElementById('result-container').classList.add('hidden');
    document.getElementById('extract-btn').disabled = true;

    try {
        const res = await fetch(`${API_BASE}/extract`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ url: url })
        });
        
        const data = await res.json();
        
        // If backend sends an error detail, throw it
        if(data.detail) throw new Error(data.detail);
        
        // Render the cards!
        renderRecipe(data, 'result-container');
    } catch (error) {
        alert("Error: " + error.message);
    } finally {
        // Always hide loader and re-enable button
        document.getElementById('loader').classList.add('hidden');
        document.getElementById('extract-btn').disabled = false;
    }
}

function renderRecipe(data, targetId) {
    const container = document.getElementById(targetId);
    
    container.innerHTML = `
        <div class="card">
            <h2>${data.title} <span class="badge">${data.difficulty}</span></h2>
            <p><strong>Cuisine:</strong> ${data.cuisine} | <strong>Time:</strong> ${data.prep_time} prep, ${data.cook_time} cook</p>
            <p><strong>Servings:</strong> ${data.servings}</p>
        </div>
        
        <div class="grid">
            <div class="card">
                <h3>Ingredients</h3>
                <ul>${data.ingredients.map(i => `<li>${i.quantity} ${i.unit} ${i.item}</li>`).join('')}</ul>
            </div>
            <div class="card">
                <h3>Nutrition / serving</h3>
                <p>Cal: ${data.nutrition_estimate.calories} | P: ${data.nutrition_estimate.protein} | C: ${data.nutrition_estimate.carbs} | F: ${data.nutrition_estimate.fat}</p>
            </div>
        </div>
        
        <div class="card">
            <h3>Instructions</h3>
            <ol>${data.instructions.map(i => `<li>${i}</li>`).join('')}</ol>
        </div>
        
        <div class="card">
            <h3>Substitutions</h3>
            <ul>${data.substitutions.map(s => `<li>${s}</li>`).join('')}</ul>
        </div>
        
        <div class="card">
            <h3>Shopping List</h3>
            <pre>${JSON.stringify(data.shopping_list, null, 2)}</pre>
        </div>
        
        <div class="card">
            <h3>Pairings</h3>
            <ul>${data.related_recipes.map(r => `<li>${r}</li>`).join('')}</ul>
        </div>
    `;
    
    container.classList.remove('hidden');
}

async function loadHistory() {
    try {
        const res = await fetch(`${API_BASE}/recipes`);
        const recipes = await res.json();
        const tbody = document.querySelector('#history-table tbody');
        
        tbody.innerHTML = recipes.map(r => `
            <tr>
                <td>${r.title}</td>
                <td>${r.cuisine}</td>
                <td>${r.difficulty}</td>
                <td>${new Date(r.created_at).toLocaleDateString()}</td>
                <td><button onclick="viewDetails(${r.id})">Details</button></td>
            </tr>
        `).join('');
    } catch (e) {
        console.error("Failed to load history", e);
    }
}

async function viewDetails(id) {
    try {
        const res = await fetch(`${API_BASE}/recipes/${id}`);
        const data = await res.json();
        renderRecipe(data, 'modal-body');
        document.getElementById('modal').classList.remove('hidden');
    } catch (e) {
        alert("Failed to load details");
    }
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
}