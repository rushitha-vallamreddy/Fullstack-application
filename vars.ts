export type KV = { key: string; value: string; enabled: boolean };

export type AuthType = "none" | "bearer" | "basic";
export type BodyMode = "none" | "raw" | "form-data" | "x-www-form-urlencoded";
export type RawType = "json" | "text";

export type SavedRequest = {
  id: number;
  collection_id: number | null;
  name: string;
  method: string;
  url: string;
  params: string;      // JSON string of KV[]
  headers: string;     // JSON string of KV[]
  body_mode: BodyMode;
  body: string;
  raw_type: RawType;
  auth_type: AuthType;
  auth_data: string;   // JSON
};

export type Collection = {
  id: number;
  name: string;
  created_at: string;
  requests: SavedRequest[];
};

export type EnvVariable = {
  id?: number;
  key: string;
  value: string;
  enabled: boolean;
};

export type Environment = {
  id: number;
  name: string;
  is_active: boolean;
  variables: EnvVariable[];
};

export type HistoryEntry = {
  id: number;
  method: string;
  url: string;
  status_code: number | null;
  time_ms: number;
  size_bytes: number;
  request_snapshot: string;
  created_at: string;
};

export type SendResponse = {
  status_code: number;
  status_text: string;
  time_ms: number;
  size_bytes: number;
  headers: Record<string, string>;
  body: string;
  content_type: string;
};

// In-memory tab state
export type Tab = {
  id: string;
  savedRequestId: number | null;   // null = unsaved
  collectionId: number | null;
  name: string;
  method: string;
  url: string;
  params: KV[];
  headers: KV[];
  bodyMode: BodyMode;
  body: string;
  rawType: RawType;
  authType: AuthType;
  authData: { token?: string; username?: string; password?: string };
  dirty: boolean;
  response?: SendResponse | null;
  loading?: boolean;
  error?: string | null;
};

export const HTTP_METHODS = [
  "GET",
  "POST",
  "PUT",
  "PATCH",
  "DELETE",
  "HEAD",
  "OPTIONS",
];
