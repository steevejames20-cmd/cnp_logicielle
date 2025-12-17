const API_BASE = "http://localhost:8000";

async function api(method, path, body) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${API_BASE}${path}`, opts);
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || res.statusText);
  }
  return res.json();
}

function bindForm(formId, handler) {
  const form = document.getElementById(formId);
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    try {
      await handler(data);
      form.reset();
    } catch (err) {
      alert(err.message);
    }
  });
}

async function renderBudgets() {
  const container = document.getElementById("budget-list");
  if (!container) return;
  const budgets = await api("GET", "/budget");
  container.innerHTML = budgets
    .map(
      (b) => `<div class="card">
        <strong>${b.name}</strong> — ${b.amount} (${b.period})
        <div>Dépenses: ${b.expenses?.length || 0}</div>
      </div>`
    )
    .join("");
}

async function renderExpenses() {
  const container = document.getElementById("expense-list");
  if (!container) return;
  const expenses = await api("GET", "/expense");
  container.innerHTML = expenses
    .map(
      (e) => `<div class="card">
        <strong>${e.category}</strong> — ${e.amount} (Budget #${e.budget_id})
        <div>${e.description || ""}</div>
      </div>`
    )
    .join("");
}

async function renderSavings() {
  const container = document.getElementById("saving-list");
  if (!container) return;
  const goals = await api("GET", "/saving-goal");
  container.innerHTML = goals
    .map(
      (g) => `<div class="card">
        <strong>${g.name}</strong> — ${g.saved_amount}/${g.target_amount}
        <div>Deadline: ${g.deadline || "N/A"}</div>
      </div>`
    )
    .join("");
}

async function renderAdvice() {
  const basicContainer = document.getElementById("advice-basic");
  const advContainer = document.getElementById("advice-advanced");
  if (basicContainer) {
    const basic = await api("GET", "/advice/basic");
    basicContainer.innerHTML = basic
      .map(
        (a) => `<div class="card ${a.severity}">
          ${a.advice_text}
        </div>`
      )
      .join("");
  }
  if (advContainer) {
    try {
      const advanced = await api("GET", "/advice/advanced");
      advContainer.innerHTML = advanced
        .map((a) => `<div class="card ${a.severity}">${a.advice_text}</div>`)
        .join("");
    } catch (err) {
      advContainer.innerHTML = `<div class="card">Premium requis pour les conseils avancés.</div>`;
    }
  }
}

function initPage() {
  const page = document.body.dataset.page;
  if (page === "budget") {
    bindForm("budget-form", (data) =>
      api("POST", "/budget", {
        name: data.name,
        amount: parseFloat(data.amount),
        period: data.period,
      }).then(renderBudgets)
    );
    renderBudgets();
  }
  if (page === "expenses") {
    bindForm("expense-form", (data) =>
      api("POST", "/expense", {
        budget_id: parseInt(data.budget_id, 10),
        amount: parseFloat(data.amount),
        category: data.category,
        payment_method: data.payment_method,
        description: data.description,
      }).then(renderExpenses)
    );
    renderExpenses();
  }
  if (page === "savings") {
    bindForm("saving-form", (data) =>
      api("POST", "/saving-goal", {
        name: data.name,
        target_amount: parseFloat(data.target_amount),
        saved_amount: parseFloat(data.saved_amount || 0),
        deadline: data.deadline || null,
      }).then(renderSavings)
    );
    renderSavings();
  }
  if (page === "advice") {
    renderAdvice();
  }
}

document.addEventListener("DOMContentLoaded", initPage);

const API_BASE = "http://localhost:8000";

async function api(method, path, body) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(`${API_BASE}${path}`, opts);
  if (!res.ok) {
    const msg = await res.text();
    throw new Error(msg || res.statusText);
  }
  return res.json();
}

function bindForm(formId, handler) {
  const form = document.getElementById(formId);
  if (!form) return;
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const data = Object.fromEntries(new FormData(form));
    try {
      await handler(data);
      form.reset();
    } catch (err) {
      alert(err.message);
    }
  });
}

async function renderBudgets() {
  const container = document.getElementById("budget-list");
  if (!container) return;
  const budgets = await api("GET", "/budget");
  container.innerHTML = budgets
    .map(
      (b) => `<div class="card">
        <strong>${b.name}</strong> — ${b.amount} (${b.period})
        <div>Dépenses: ${b.expenses?.length || 0}</div>
      </div>`
    )
    .join("");
}

async function renderExpenses() {
  const container = document.getElementById("expense-list");
  if (!container) return;
  const expenses = await api("GET", "/expense");
  container.innerHTML = expenses
    .map(
      (e) => `<div class="card">
        <strong>${e.category}</strong> — ${e.amount} (Budget #${e.budget_id})
        <div>${e.description || ""}</div>
      </div>`
    )
    .join("");
}

async function renderSavings() {
  const container = document.getElementById("saving-list");
  if (!container) return;
  const goals = await api("GET", "/saving-goal");
  container.innerHTML = goals
    .map(
      (g) => `<div class="card">
        <strong>${g.name}</strong> — ${g.saved_amount}/${g.target_amount}
        <div>Deadline: ${g.deadline || "N/A"}</div>
      </div>`
    )
    .join("");
}

async function renderAdvice() {
  const basicContainer = document.getElementById("advice-basic");
  const advContainer = document.getElementById("advice-advanced");
  if (basicContainer) {
    const basic = await api("GET", "/advice/basic");
    basicContainer.innerHTML = basic
      .map(
        (a) => `<div class="card ${a.severity}">
          ${a.advice_text}
        </div>`
      )
      .join("");
  }
  if (advContainer) {
    try {
      const advanced = await api("GET", "/advice/advanced");
      advContainer.innerHTML = advanced
        .map((a) => `<div class="card ${a.severity}">${a.advice_text}</div>`)
        .join("");
    } catch (err) {
      advContainer.innerHTML = `<div class="card">Premium requis pour les conseils avancés.</div>`;
    }
  }
}

function initPage() {
  const page = document.body.dataset.page;
  if (page === "budget") {
    bindForm("budget-form", (data) =>
      api("POST", "/budget", {
        name: data.name,
        amount: parseFloat(data.amount),
        period: data.period,
      }).then(renderBudgets)
    );
    renderBudgets();
  }
  if (page === "expenses") {
    bindForm("expense-form", (data) =>
      api("POST", "/expense", {
        budget_id: parseInt(data.budget_id, 10),
        amount: parseFloat(data.amount),
        category: data.category,
        payment_method: data.payment_method,
        description: data.description,
      }).then(renderExpenses)
    );
    renderExpenses();
  }
  if (page === "savings") {
    bindForm("saving-form", (data) =>
      api("POST", "/saving-goal", {
        name: data.name,
        target_amount: parseFloat(data.target_amount),
        saved_amount: parseFloat(data.saved_amount || 0),
        deadline: data.deadline || null,
      }).then(renderSavings)
    );
    renderSavings();
  }
  if (page === "advice") {
    renderAdvice();
  }
}

document.addEventListener("DOMContentLoaded", initPage);


