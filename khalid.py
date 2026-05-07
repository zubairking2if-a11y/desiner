from http.server import HTTPServer, SimpleHTTPRequestHandler
import socket

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cost Management System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        
        .navbar {
            background: #333;
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        
        .navbar h1 {
            font-size: 24px;
        }
        
        .nav-buttons {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        
        .auth-buttons {
            display: flex;
            gap: 10px;
        }
        
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: #667eea;
            color: white;
        }
        
        .btn-primary:hover {
            background: #5568d3;
        }
        
        .btn-secondary {
            background: #e0e0e0;
            color: #333;
        }
        
        .btn-secondary:hover {
            background: #d0d0d0;
        }
        
        .btn-danger {
            background: #dc3545;
            color: white;
        }
        
        .btn-danger:hover {
            background: #c82333;
        }
        
        .btn-info {
            background: #17a2b8;
            color: white;
        }
        
        .btn-info:hover {
            background: #138496;
        }
        
        .content {
            padding: 30px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
        }
        
        .content.full-width {
            grid-template-columns: 1fr;
        }
        
        .section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .section h2 {
            margin-bottom: 20px;
            color: #333;
            font-size: 20px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #555;
            font-weight: 500;
        }
        
        .form-group input,
        .form-group select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        
        .form-group input:focus,
        .form-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.3);
        }
        
        .form-actions {
            display: flex;
            gap: 10px;
            margin-top: 20px;
        }
        
        .form-actions button {
            flex: 1;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .table th {
            background: #667eea;
            color: white;
            padding: 12px;
            text-align: left;
        }
        
        .table td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        
        .table tr:hover {
            background: #f0f0f0;
        }
        
        .calculation {
            background: #e8f4f8;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
            border-left: 4px solid #17a2b8;
        }
        
        .calculation h4 {
            color: #17a2b8;
            margin-bottom: 10px;
        }
        
        .calculation p {
            font-size: 16px;
            color: #333;
            font-weight: bold;
        }
        
        .meaning {
            background: #fff3cd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ffc107;
        }
        
        .meaning h3 {
            color: #856404;
            margin-bottom: 10px;
        }
        
        .meaning-item {
            color: #856404;
            margin: 5px 0;
            padding-left: 20px;
        }
        
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
        }
        
        .modal.show {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .modal-content {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            max-width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            width: 100%;
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 15px;
        }
        
        .modal-header h2 {
            color: #333;
        }
        
        .close-btn {
            background: #dc3545;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        
        .close-btn:hover {
            background: #c82333;
        }
        
        .records-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-card h3 {
            font-size: 32px;
            margin-bottom: 5px;
        }
        
        .stat-card p {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .records-tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ddd;
        }
        
        .tab-btn {
            padding: 12px 20px;
            background: none;
            border: none;
            color: #666;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
        }
        
        .tab-btn.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .export-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #ddd;
        }
        
        .export-btn {
            background: #28a745;
            color: white;
        }
        
        .export-btn:hover {
            background: #218838;
        }
        
        @media (max-width: 768px) {
            .content {
                grid-template-columns: 1fr;
            }
            
            .navbar {
                flex-direction: column;
            }
            
            .nav-buttons {
                width: 100%;
                justify-content: space-between;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Navbar -->
        <div class="navbar">
            <h1>💰 Cost Management System</h1>
            <div class="nav-buttons">
                <div class="auth-buttons">
                    <button class="btn btn-secondary" onclick="showLogin()">Login</button>
                    <button class="btn btn-primary" onclick="showSignin()">Sign In</button>
                </div>
                <button class="btn btn-info" onclick="openAllRecords()">👁️ See All Records</button>
            </div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            <!-- New Customer Section -->
            <div class="section">
                <h2>➕ New Customer</h2>
                <form id="customerForm">
                    <div class="form-group">
                        <label for="customerName">Customer Name:</label>
                        <input type="text" id="customerName" placeholder="Enter customer name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="customerAdd">Customer Address:</label>
                        <input type="text" id="customerAdd" placeholder="Enter address" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="wayPrice">Ways Price (W.P):</label>
                        <input type="number" id="wayPrice" placeholder="Enter price" step="0.01" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="wayUse">Ways Use (W.U):</label>
                        <input type="number" id="wayUse" placeholder="Enter usage" step="0.01" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="custModem">Customer Modem (C.M):</label>
                        <input type="number" id="custModem" placeholder="Enter modem cost" step="0.01" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="custPackage">Customer Package (C.P):</label>
                        <input type="number" id="custPackage" placeholder="Enter package cost" step="0.01" required>
                    </div>
                    
                    <div class="calculation">
                        <h4>Formula: W.P × W.U + C.M + C.P = Total</h4>
                        <p id="totalCost">Total: $0.00</p>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="btn btn-primary" onclick="saveCustomer()">Save Customer</button>
                        <button type="button" class="btn btn-secondary" onclick="resetForm()">Reset</button>
                    </div>
                </form>
            </div>
            
            <!-- Campaign Section -->
            <div class="section">
                <h2>📊 Campaign</h2>
                <form id="campaignForm">
                    <div class="form-group">
                        <label for="campaignName">Campaign Name:</label>
                        <input type="text" id="campaignName" placeholder="Enter campaign name" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="campaignAdd">Campaign Address:</label>
                        <input type="text" id="campaignAdd" placeholder="Enter address" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="tool1Price">Tool 1 Price:</label>
                        <input type="number" id="tool1Price" placeholder="Enter price" step="0.01" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="tool1Use">Tool 1 Use:</label>
                        <input type="number" id="tool1Use" placeholder="Enter usage" step="0.01" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="tool2Price">Tool 2 Price:</label>
                        <input type="number" id="tool2Price" placeholder="Enter price" step="0.01" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="tool2Use">Tool 2 Use:</label>
                        <input type="number" id="tool2Use" placeholder="Enter usage" step="0.01" required>
                    </div>
                    
                    <div class="calculation">
                        <h4>Formula: Price.1 + Price.2 = Total</h4>
                        <p id="campaignTotal">Total: $0.00</p>
                    </div>
                    
                    <div class="form-actions">
                        <button type="button" class="btn btn-primary" onclick="saveCampaign()">Save Campaign</button>
                        <button type="button" class="btn btn-secondary" onclick="resetCampaignForm()">Reset</button>
                    </div>
                </form>
            </div>
            
            <!-- Meaning Section (Full Width) -->
            <div class="section" style="grid-column: 1 / -1;">
                <h2>📝 Abbreviations & Meanings</h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
                    <div class="meaning-item"><strong>C</strong> = Customer</div>
                    <div class="meaning-item"><strong>P</strong> = Price</div>
                    <div class="meaning-item"><strong>U</strong> = Use</div>
                    <div class="meaning-item"><strong>M</strong> = Modem</div>
                    <div class="meaning-item"><strong>W</strong> = Ways</div>
                </div>
            </div>
            
            <!-- Saved Data Section (Full Width) -->
            <div class="section" style="grid-column: 1 / -1;">
                <h2>📋 Saved Customers</h2>
                <table class="table" id="customerTable">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Address</th>
                            <th>Total Cost</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="customerTableBody">
                    </tbody>
                </table>
            </div>
            
            <div class="section" style="grid-column: 1 / -1;">
                <h2>📋 Saved Campaigns</h2>
                <table class="table" id="campaignTable">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Address</th>
                            <th>Total Cost</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="campaignTableBody">
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- See All Records Modal -->
    <div id="allRecordsModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>📊 All Records Overview</h2>
                <button class="close-btn" onclick="closeAllRecords()">✕ Close</button>
            </div>
            
            <!-- Statistics Cards -->
            <div class="records-stats">
                <div class="stat-card">
                    <h3 id="totalCustomers">0</h3>
                    <p>Total Customers</p>
                </div>
                <div class="stat-card">
                    <h3 id="totalCampaigns">0</h3>
                    <p>Total Campaigns</p>
                </div>
                <div class="stat-card">
                    <h3 id="totalRecords">0</h3>
                    <p>Total Records</p>
                </div>
                <div class="stat-card">
                    <h3 id="totalRevenue">$0.00</h3>
                    <p>Total Revenue</p>
                </div>
            </div>
            
            <!-- Tab Navigation -->
            <div class="records-tabs">
                <button class="tab-btn active" onclick="switchTab('customers-tab')">👥 Customers</button>
                <button class="tab-btn" onclick="switchTab('campaigns-tab')">📊 Campaigns</button>
                <button class="tab-btn" onclick="switchTab('summary-tab')">📈 Summary</button>
            </div>
            
            <!-- Customers Tab -->
            <div id="customers-tab" class="tab-content active">
                <h3>All Customers Records</h3>
                <table class="table" id="allCustomersTable">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Address</th>
                            <th>Ways Price</th>
                            <th>Ways Use</th>
                            <th>Modem</th>
                            <th>Package</th>
                            <th>Total Cost</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="allCustomersTableBody">
                    </tbody>
                </table>
            </div>
            
            <!-- Campaigns Tab -->
            <div id="campaigns-tab" class="tab-content">
                <h3>All Campaigns Records</h3>
                <table class="table" id="allCampaignsTable">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Address</th>
                            <th>Tool 1 Price</th>
                            <th>Tool 2 Price</th>
                            <th>Total Cost</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="allCampaignsTableBody">
                    </tbody>
                </table>
            </div>
            
            <!-- Summary Tab -->
            <div id="summary-tab" class="tab-content">
                <h3>Financial Summary</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 20px;">
                    <div class="calculation">
                        <h4>Customers Summary</h4>
                        <p>Total Customers: <strong id="summaryCustomers">0</strong></p>
                        <p>Average Cost: <strong>$<span id="avgCustomerCost">0.00</span></strong></p>
                        <p>Total: <strong>$<span id="sumCustomerCost">0.00</span></strong></p>
                    </div>
                    <div class="calculation">
                        <h4>Campaigns Summary</h4>
                        <p>Total Campaigns: <strong id="summaryCampaigns">0</strong></p>
                        <p>Average Cost: <strong>$<span id="avgCampaignCost">0.00</span></strong></p>
                        <p>Total: <strong>$<span id="sumCampaignCost">0.00</span></strong></p>
                    </div>
                </div>
            </div>
            
            <!-- Export Section -->
            <div class="export-section">
                <button class="btn export-btn" onclick="exportToCSV()">📥 Export to CSV</button>
                <button class="btn btn-info" onclick="printRecords()">🖨️ Print Records</button>
            </div>
        </div>
    </div>
    
    <script>
        // Data storage
        let customers = JSON.parse(localStorage.getItem('customers')) || [];
        let campaigns = JSON.parse(localStorage.getItem('campaigns')) || [];
        
        // Calculate customer total
        function calculateCustomerTotal() {
            const wayPrice = parseFloat(document.getElementById('wayPrice').value) || 0;
            const wayUse = parseFloat(document.getElementById('wayUse').value) || 0;
            const custModem = parseFloat(document.getElementById('custModem').value) || 0;
            const custPackage = parseFloat(document.getElementById('custPackage').value) || 0;
            
            const total = (wayPrice * wayUse) + custModem + custPackage;
            document.getElementById('totalCost').textContent = `Total: $${total.toFixed(2)}`;
        }
        
        // Calculate campaign total
        function calculateCampaignTotal() {
            const tool1Price = parseFloat(document.getElementById('tool1Price').value) || 0;
            const tool2Price = parseFloat(document.getElementById('tool2Price').value) || 0;
            
            const total = tool1Price + tool2Price;
            document.getElementById('campaignTotal').textContent = `Total: $${total.toFixed(2)}`;
        }
        
        // Save customer
        function saveCustomer() {
            const customer = {
                id: Date.now(),
                name: document.getElementById('customerName').value,
                address: document.getElementById('customerAdd').value,
                wayPrice: parseFloat(document.getElementById('wayPrice').value),
                wayUse: parseFloat(document.getElementById('wayUse').value),
                modem: parseFloat(document.getElementById('custModem').value),
                package: parseFloat(document.getElementById('custPackage').value),
                total: (parseFloat(document.getElementById('wayPrice').value) * parseFloat(document.getElementById('wayUse').value)) + parseFloat(document.getElementById('custModem').value) + parseFloat(document.getElementById('custPackage').value)
            };
            
            customers.push(customer);
            localStorage.setItem('customers', JSON.stringify(customers));
            resetForm();
            displayCustomers();
            alert('Customer saved successfully!');
        }
        
        // Save campaign
        function saveCampaign() {
            const campaign = {
                id: Date.now(),
                name: document.getElementById('campaignName').value,
                address: document.getElementById('campaignAdd').value,
                tool1Price: parseFloat(document.getElementById('tool1Price').value),
                tool2Price: parseFloat(document.getElementById('tool2Price').value),
                total: parseFloat(document.getElementById('tool1Price').value) + parseFloat(document.getElementById('tool2Price').value)
            };
            
            campaigns.push(campaign);
            localStorage.setItem('campaigns', JSON.stringify(campaigns));
            resetCampaignForm();
            displayCampaigns();
            alert('Campaign saved successfully!');
        }
        
        // Display customers in table
        function displayCustomers() {
            const tbody = document.getElementById('customerTableBody');
            tbody.innerHTML = '';
            customers.forEach(customer => {
                tbody.innerHTML += `
                    <tr>
                        <td>${customer.name}</td>
                        <td>${customer.address}</td>
                        <td>$${customer.total.toFixed(2)}</td>
                        <td>
                            <button class="btn btn-secondary" onclick="editCustomer(${customer.id})">Edit</button>
                            <button class="btn btn-danger" onclick="deleteCustomer(${customer.id})">Delete</button>
                        </td>
                    </tr>
                `;
            });
        }
        
        // Display campaigns in table
        function displayCampaigns() {
            const tbody = document.getElementById('campaignTableBody');
            tbody.innerHTML = '';
            campaigns.forEach(campaign => {
                tbody.innerHTML += `
                    <tr>
                        <td>${campaign.name}</td>
                        <td>${campaign.address}</td>
                        <td>$${campaign.total.toFixed(2)}</td>
                        <td>
                            <button class="btn btn-secondary" onclick="editCampaign(${campaign.id})">Edit</button>
                            <button class="btn btn-danger" onclick="deleteCampaign(${campaign.id})">Delete</button>
                        </td>
                    </tr>
                `;
            });
        }
        
        // Delete customer
        function deleteCustomer(id) {
            if(confirm('Are you sure?')) {
                customers = customers.filter(c => c.id !== id);
                localStorage.setItem('customers', JSON.stringify(customers));
                displayCustomers();
            }
        }
        
        // Delete campaign
        function deleteCampaign(id) {
            if(confirm('Are you sure?')) {
                campaigns = campaigns.filter(c => c.id !== id);
                localStorage.setItem('campaigns', JSON.stringify(campaigns));
                displayCampaigns();
            }
        }
        
        // Reset forms
        function resetForm() {
            document.getElementById('customerForm').reset();
            document.getElementById('totalCost').textContent = 'Total: $0.00';
        }
        
        function resetCampaignForm() {
            document.getElementById('campaignForm').reset();
            document.getElementById('campaignTotal').textContent = 'Total: $0.00';
        }
        
        // Auth functions
        function showLogin() {
            alert('Login functionality would be implemented here');
        }
        
        function showSignin() {
            alert('Sign In functionality would be implemented here');
        }
        
        // Open All Records Modal
        function openAllRecords() {
            document.getElementById('allRecordsModal').classList.add('show');
            updateAllRecords();
        }
        
        // Close All Records Modal
        function closeAllRecords() {
            document.getElementById('allRecordsModal').classList.remove('show');
        }
        
        // Switch between tabs
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from all buttons
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked button
            event.target.classList.add('active');
        }
        
        // Update all records display
        function updateAllRecords() {
            // Update statistics
            document.getElementById('totalCustomers').textContent = customers.length;
            document.getElementById('totalCampaigns').textContent = campaigns.length;
            document.getElementById('totalRecords').textContent = customers.length + campaigns.length;
            
            const totalRevenue = customers.reduce((sum, c) => sum + c.total, 0) + 
                                campaigns.reduce((sum, c) => sum + c.total, 0);
            document.getElementById('totalRevenue').textContent = `$${totalRevenue.toFixed(2)}`;
            
            // Display all customers
            const allCustomersTableBody = document.getElementById('allCustomersTableBody');
            allCustomersTableBody.innerHTML = '';
            customers.forEach((customer, index) => {
                allCustomersTableBody.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${customer.name}</td>
                        <td>${customer.address}</td>
                        <td>$${customer.wayPrice.toFixed(2)}</td>
                        <td>${customer.wayUse}</td>
                        <td>$${customer.modem.toFixed(2)}</td>
                        <td>$${customer.package.toFixed(2)}</td>
                        <td><strong>$${customer.total.toFixed(2)}</strong></td>
                        <td>
                            <button class="btn btn-danger" onclick="deleteCustomerFromModal(${customer.id})">Delete</button>
                        </td>
                    </tr>
                `;
            });
            
            // Display all campaigns
            const allCampaignsTableBody = document.getElementById('allCampaignsTableBody');
            allCampaignsTableBody.innerHTML = '';
            campaigns.forEach((campaign, index) => {
                allCampaignsTableBody.innerHTML += `
                    <tr>
                        <td>${index + 1}</td>
                        <td>${campaign.name}</td>
                        <td>${campaign.address}</td>
                        <td>$${campaign.tool1Price.toFixed(2)}</td>
                        <td>$${campaign.tool2Price.toFixed(2)}</td>
                        <td><strong>$${campaign.total.toFixed(2)}</strong></td>
                        <td>
                            <button class="btn btn-danger" onclick="deleteCampaignFromModal(${campaign.id})">Delete</button>
                        </td>
                    </tr>
                `;
            });
            
            // Update summary
            document.getElementById('summaryCustomers').textContent = customers.length;
            document.getElementById('summaryCampaigns').textContent = campaigns.length;
            
            const avgCustomer = customers.length > 0 ? customers.reduce((sum, c) => sum + c.total, 0) / customers.length : 0;
            const sumCustomer = customers.reduce((sum, c) => sum + c.total, 0);
            document.getElementById('avgCustomerCost').textContent = avgCustomer.toFixed(2);
            document.getElementById('sumCustomerCost').textContent = sumCustomer.toFixed(2);
            
            const avgCampaign = campaigns.length > 0 ? campaigns.reduce((sum, c) => sum + c.total, 0) / campaigns.length : 0;
            const sumCampaign = campaigns.reduce((sum, c) => sum + c.total, 0);
            document.getElementById('avgCampaignCost').textContent = avgCampaign.toFixed(2);
            document.getElementById('sumCampaignCost').textContent = sumCampaign.toFixed(2);
        }
        
        // Delete from modal
        function deleteCustomerFromModal(id) {
            if(confirm('Are you sure?')) {
                customers = customers.filter(c => c.id !== id);
                localStorage.setItem('customers', JSON.stringify(customers));
                displayCustomers();
                updateAllRecords();
            }
        }
        
        function deleteCampaignFromModal(id) {
            if(confirm('Are you sure?')) {
                campaigns = campaigns.filter(c => c.id !== id);
                localStorage.setItem('campaigns', JSON.stringify(campaigns));
                displayCampaigns();
                updateAllRecords();
            }
        }
        
        // Export to CSV
        function exportToCSV() {
            let csvContent = "data:text/csv;charset=utf-8,";
            
            // Add customers
            csvContent += "CUSTOMERS\\n";
            csvContent += "Name,Address,Ways Price,Ways Use,Modem,Package,Total\\n";
            customers.forEach(customer => {
                csvContent += `${customer.name},${customer.address},${customer.wayPrice},${customer.wayUse},${customer.modem},${customer.package},${customer.total}\\n`;
            });
            
            csvContent += "\\n\\nCAMPAIGNS\\n";
            csvContent += "Name,Address,Tool 1 Price,Tool 2 Price,Total\\n";
            campaigns.forEach(campaign => {
                csvContent += `${campaign.name},${campaign.address},${campaign.tool1Price},${campaign.tool2Price},${campaign.total}\\n`;
            });
            
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "records.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
        
        // Print records
        function printRecords() {
            window.print();
        }
        
        // Close modal when clicking outside
        window.onclick = function(event) {
            const modal = document.getElementById('allRecordsModal');
            if (event.target == modal) {
                modal.classList.remove('show');
            }
        }
        
        // Event listeners for real-time calculation
        document.getElementById('wayPrice').addEventListener('input', calculateCustomerTotal);
        document.getElementById('wayUse').addEventListener('input', calculateCustomerTotal);
        document.getElementById('custModem').addEventListener('input', calculateCustomerTotal);
        document.getElementById('custPackage').addEventListener('input', calculateCustomerTotal);
        
        document.getElementById('tool1Price').addEventListener('input', calculateCampaignTotal);
        document.getElementById('tool2Price').addEventListener('input', calculateCampaignTotal);
        
        // Load data on page load
        window.addEventListener('load', function() {
            displayCustomers();
            displayCampaigns();
        });
    </script>
</body>
</html>
"""

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()

def find_available_port(start_port=8000):
    """Find an available port starting from start_port"""
    port = start_port
    while port < start_port + 100:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', port))
            sock.close()
            return port
        except OSError:
            port += 1
    return None

def run_server(port=None):
    if port is None:
        port = find_available_port(8000)
    
    if port is None:
        print("❌ No available ports found!")
        return
    
    server_address = ('', port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print(f"✅ Server running!")
    print(f"🚀 Open your browser and go to: http://localhost:{port}")
    print(f"📍 Server Address: http://0.0.0.0:{port}")
    print("⏹️  Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n✋ Server stopped!")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
