import type {
  Collection,
  Environment,
  HistoryEntry,
  SavedRequest,
  SendResponse,
} from "./types";

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

async function j<T>(r: Response): Promise<T> {
  if (!r.ok) {
    let msg = r.statusText;
    try {
      const d = await r.json();
      msg = d.detail || msg;
    } catch {}
    throw new Error(msg);
  }
  return r.json();
}

export const api = {
  // collections
  listCollections: () => fetch(`${API_BASE}/collections`).then(j<Collection[]>),
  createCollection: (name: string) =>
    fetch(`${API_BASE}/collections`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }).then(j<Collection>),
  renameCollection: (id: number, name: string) =>
    fetch(`${API_BASE}/collections/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    }).then(j<Collection>),
  deleteCollection: (id: number) =>
    fetch(`${API_BASE}/collections/${id}`, { method: "DELETE" }).then(j),

  // requests
  saveRequest: (r: Partial<SavedRequest>) =>
    fetch(`${API_BASE}/requests`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(r),
    }).then(j<SavedRequest>),
  updateRequest: (id: number, r: Partial<SavedRequest>) =>
    fetch(`${API_BASE}/requests/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(r),
    }).then(j<SavedRequest>),
  deleteRequest: (id: number) =>
    fetch(`${API_BASE}/requests/${id}`, { method: "DELETE" }).then(j),

  // environments
  listEnvironments: () =>
    fetch(`${API_BASE}/environments`).then(j<Environment[]>),
  createEnvironment: (name: string, variables: any[] = []) =>
    fetch(`${API_BASE}/environments`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, variables }),
    }).then(j<Environment>),
  updateEnvironment: (id: number, data: any) =>
    fetch(`${API_BASE}/environments/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then(j<Environment>),
  deleteEnvironment: (id: number) =>
    fetch(`${API_BASE}/environments/${id}`, { method: "DELETE" }).then(j),

  // history
  listHistory: () => fetch(`${API_BASE}/history`).then(j<HistoryEntry[]>),
  clearHistory: () => fetch(`${API_BASE}/history`, { method: "DELETE" }).then(j),

  // send
  send: (payload: any) =>
    fetch(`${API_BASE}/send`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }).then(j<SendResponse>),
};
