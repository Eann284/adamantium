import { MaterialRequest } from "@/src/types/materialRequest";
import React from "react";
import RequestCard from "./RequestCard";

interface Props {
  pendingRequests: MaterialRequest[];
  onView: (request: MaterialRequest) => void;
}

function PendingList({ pendingRequests, onView }: Props) {
  return (
    <section className="ring ring-gray-200 rounded-lg p-4 overflow-y-auto h-full min-h-0">
      <h1 className="text-xl font-semibold mb-2">Requests For Approval</h1>

      <ul className="flex flex-col gap-2">
        {pendingRequests.map((req) => (
          <li key={req.mrf_id}>
            <RequestCard requests={req} onView={() => onView(req)} />
          </li>
        ))}
      </ul>
    </section>
  );
}

export default PendingList;
