

export interface MRFItem {
    product_id: number;
    quantity: number;
}

export interface MRF {
    items: MRFItem[];
    mrf_files: string |null;
}

export type ApprovalStatus =
  | "Pending"
  | "Approved"
  | "Not Approved";

export type ReleaseStatus =
  | "Pending"
  | "Released"
  | "Not Released";

  export interface MaterialRequest {
  mrf_id: number;
  requestor_email: string;
  date: string;
  approval_status: ApprovalStatus;
  approved_by: string | null;
  release_status: ReleaseStatus;
  released_by: string | null;
  mrf_files: string;
  items: MRFItem[];
}
