// FixRoute Core API Client & Session Manager

const API_BASE = "";

class FixRouteAPI {
  constructor() {
    this.token = localStorage.getItem("fixroute_token") || null;
    this.user = JSON.parse(localStorage.getItem("fixroute_user") || "null");
  }

  setSession(token, user) {
    this.token = token;
    this.user = user;
    localStorage.setItem("fixroute_token", token);
    localStorage.setItem("fixroute_user", JSON.stringify(user));
    window.dispatchEvent(new CustomEvent("fixroute:auth-change", { detail: { user } }));
  }

  clearSession() {
    this.token = null;
    this.user = null;
    localStorage.removeItem("fixroute_token");
    localStorage.removeItem("fixroute_user");
    window.dispatchEvent(new CustomEvent("fixroute:auth-change", { detail: { user: null } }));
  }

  isAuthenticated() {
    return !!this.token;
  }

  isAdmin() {
    return this.user && this.user.role === "admin";
  }

  async request(endpoint, options = {}) {
    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {})
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
      });

      if (response.status === 401 && this.token) {
        // Token expired or invalid
        this.clearSession();
      }

      const contentType = response.headers.get("content-type");
      let data = null;
      if (contentType && contentType.includes("application/json")) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      if (!response.ok) {
        const errorDetail = (data && data.detail) || response.statusText || "Request failed";
        throw new Error(typeof errorDetail === "string" ? errorDetail : JSON.stringify(errorDetail));
      }

      return data;
    } catch (err) {
      console.error(`API Error [${endpoint}]:`, err);
      throw err;
    }
  }

  // Auth Endpoints
  async register(email, fullName, password) {
    const res = await this.request("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, full_name: fullName, password })
    });
    this.setSession(res.access_token, res.user);
    return res;
  }

  async login(email, password) {
    const res = await this.request("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
    this.setSession(res.access_token, res.user);
    return res;
  }

  async getMe() {
    return await this.request("/api/auth/me");
  }

  async deleteAccount() {
    const res = await this.request("/api/auth/delete-account", { method: "DELETE" });
    this.clearSession();
    return res;
  }

  // Search & Categories
  async search(query, categorySlug = null, state = null, city = null, provider = null) {
    return await this.request("/api/search", {
      method: "POST",
      body: JSON.stringify({
        query,
        category_slug: categorySlug,
        state,
        city,
        contacted_provider: provider
      })
    });
  }

  async getCategories() {
    return await this.request("/api/categories");
  }

  async getCategory(slug) {
    return await this.request(`/api/categories/${slug}`);
  }

  async getRoute(idOrSlug) {
    return await this.request(`/api/routes/${idOrSlug}`);
  }

  // Saved Routes & History
  async getSavedRoutes() {
    return await this.request("/api/saved-routes");
  }

  async saveRoute(routeId, notes = null) {
    return await this.request("/api/saved-routes", {
      method: "POST",
      body: JSON.stringify({ route_id: routeId, notes })
    });
  }

  async unsaveRoute(id) {
    return await this.request(`/api/saved-routes/${id}`, { method: "DELETE" });
  }

  async getSearchHistory() {
    return await this.request("/api/user/searches");
  }

  async clearSearchHistory() {
    return await this.request("/api/user/searches", { method: "DELETE" });
  }

  // Complaint Tracking
  async getComplaints(status = null, search = null) {
    const params = new URLSearchParams();
    if (status) params.append("status", status);
    if (search) params.append("search", search);
    const qs = params.toString() ? `?${params.toString()}` : "";
    return await this.request(`/api/complaints${qs}`);
  }

  async createComplaint(data) {
    return await this.request("/api/complaints", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }

  async getComplaint(id) {
    return await this.request(`/api/complaints/${id}`);
  }

  async updateComplaint(id, data) {
    return await this.request(`/api/complaints/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data)
    });
  }

  async deleteComplaint(id) {
    return await this.request(`/api/complaints/${id}`, { method: "DELETE" });
  }

  async updateChecklistItem(complaintId, itemId, data) {
    return await this.request(`/api/complaints/${complaintId}/checklist/${itemId}`, {
      method: "PATCH",
      body: JSON.stringify(data)
    });
  }

  async addChecklistItem(complaintId, data) {
    return await this.request(`/api/complaints/${complaintId}/checklist`, {
      method: "POST",
      body: JSON.stringify(data)
    });
  }

  // Drafts
  async generateDraft(data) {
    return await this.request("/api/complaint-drafts/generate", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }

  async getDrafts() {
    return await this.request("/api/complaint-drafts");
  }

  async saveDraft(data) {
    return await this.request("/api/complaint-drafts", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }

  async deleteDraft(id) {
    return await this.request(`/api/complaint-drafts/${id}`, { method: "DELETE" });
  }

  // Feedback & Corrections
  async submitFeedback(data) {
    return await this.request("/api/feedback", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }

  async submitCorrection(data) {
    return await this.request("/api/corrections", {
      method: "POST",
      body: JSON.stringify(data)
    });
  }

  // Admin
  async getAdminStats() {
    return await this.request("/api/admin/stats");
  }

  async getAdminRoutes() {
    return await this.request("/api/admin/routes");
  }

  async updateRouteVerification(id, status) {
    return await this.request(`/api/admin/routes/${id}/verification`, {
      method: "PUT",
      body: JSON.stringify({ verification_status: status })
    });
  }

  async getAdminCorrections() {
    return await this.request("/api/admin/corrections");
  }

  async updateAdminCorrection(id, data) {
    return await this.request(`/api/admin/corrections/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data)
    });
  }

  async getAdminFeedback() {
    return await this.request("/api/admin/feedback");
  }

  async getAdminAuditLogs() {
    return await this.request("/api/admin/audit-logs");
  }

  // AI Assistant
  async clarifyWithAI(problemText, selectedCategory = null) {
    return await this.request("/api/ai/clarify", {
      method: "POST",
      body: JSON.stringify({ problem_text: problemText, selected_category: selectedCategory })
    });
  }
}

// Global singleton instance
window.fixRoute = new FixRouteAPI();
