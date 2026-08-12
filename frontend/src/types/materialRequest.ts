type ApprovalStatus = "Pending" | "Approved" | "Not Approved"
type ReleaseStatus = "Pending" | "Released" | "Not Released"

export interface Request {
     mrf_id: number;
    requestor_email: string;
    date: string;
    approval_status: ApprovalStatus;
    approved_by: string | null;
    release_status: ReleaseStatus;
    released_by: string | null;
    mrf_files: string;
    items: Record<string, unknown>[];
}