export type OccupationItem = {
  onetsoc_code: string;
  soc_code: string;
  title: string;
  ai_mean: number | null;
  ai_std: number | null;
  employment: number | null;
  median_wage: number | null;
  ref_year_month: string | null;
};

export type OccupationDetail = {
  soc_code: string;
  onetsoc_codes: string[];
  title: string;
  description: string | null;
  alternate_titles: string[];
  top_tasks: {
    task_id: number;
    task_statement: string;
    weight: number;
  }[];
  ai_score: {
    mean: number | null;
    std: number | null;
    updated_at: string | null;
  } | null;
};

export type RankingItem = {
  soc_code: string;
  title: string;
  ai_mean: number | null;
  ai_std: number | null;
};

export type OccupationListResponse = {
  items: OccupationItem[];
  page: number;
  page_size: number;
  total: number;
};

export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE?.replace(/\/$/, "") ||
  "http://localhost:8001";

const defaultVersion = process.env.NEXT_PUBLIC_DATA_VERSION || "30.1";

export function getDataVersion(value?: string) {
  return value && value.trim() ? value.trim() : defaultVersion;
}

export async function fetchOccupations(params: {
  search?: string;
  sort?: "ai" | "employment";
  page?: number;
  pageSize?: number;
  dataVersion?: string;
  signal?: AbortSignal;
}): Promise<OccupationListResponse> {
  const searchParams = new URLSearchParams();
  if (params.search) searchParams.set("search", params.search);
  if (params.sort) searchParams.set("sort", params.sort);
  if (params.page) searchParams.set("page", String(params.page));
  if (params.pageSize) searchParams.set("page_size", String(params.pageSize));
  searchParams.set("data_version", getDataVersion(params.dataVersion));

  const response = await fetch(
    `${API_BASE}/occupations?${searchParams.toString()}`,
    { signal: params.signal }
  );
  if (!response.ok) {
    throw new Error(`Failed to load occupations (${response.status})`);
  }
  return response.json();
}

export async function fetchOccupationDetail(
  socCode: string,
  dataVersion?: string,
  signal?: AbortSignal
): Promise<OccupationDetail> {
  const searchParams = new URLSearchParams();
  searchParams.set("data_version", getDataVersion(dataVersion));
  const response = await fetch(
    `${API_BASE}/occupations/${encodeURIComponent(socCode)}?${searchParams.toString()}`,
    { signal }
  );
  if (!response.ok) {
    throw new Error(`Failed to load occupation (${response.status})`);
  }
  return response.json();
}

export async function fetchRankings(params: {
  limit?: number;
  dataVersion?: string;
  signal?: AbortSignal;
}): Promise<{ items: RankingItem[]; limit: number }> {
  const searchParams = new URLSearchParams();
  if (params.limit) searchParams.set("limit", String(params.limit));
  searchParams.set("data_version", getDataVersion(params.dataVersion));
  const response = await fetch(
    `${API_BASE}/rankings/ai_risk?${searchParams.toString()}`,
    { signal: params.signal }
  );
  if (!response.ok) {
    throw new Error(`Failed to load rankings (${response.status})`);
  }
  return response.json();
}
