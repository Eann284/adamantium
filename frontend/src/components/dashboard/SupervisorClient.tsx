"use client";

import { MaterialRequest } from "@/src/types/materialRequest";
import PendingList from "./PendingList";
import { useState } from "react";
import RequestDetails from "./RequestDetails";
import { Product } from "@/src/types/product";

interface Props {
  pending: MaterialRequest[];
  products: Product[]
  accessToken: string;
}

function SupervisorClient({ pending, products, accessToken }: Props) {
  const [selectedRequest, setSelectedRequest] =
    useState<MaterialRequest | null>(null);

  return (
    
      <main className="h-full flex flex-col p-4 gap-2">
        <div
          className="grid 
        grid-cols-2 gap-2 flex-1 min-h-0
        "
        >
          {/* left panel */}
          <section className="min-h-0">
            <PendingList
              pendingRequests={pending}
              onView={setSelectedRequest}
            />
          </section>

          {/* right panel split vertically */}

          <section className="ring ring-gray-200 rounded-lg grid grid-cols-1 p-2">
            <div className="p-2 overflow-y-auto min-h-0">
              <RequestDetails
                request={selectedRequest}
                products={products}
                accessToken={accessToken}
              />
            </div>
          </section>
        </div>
      </main>
  
  );
}

export default SupervisorClient;
