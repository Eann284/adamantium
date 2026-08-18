"use client";
import {
  approveRequest,
  disapproveRequest,
} from "@/src/services/requestService";
import { MaterialRequest } from "@/src/types/materialRequest";
import React, { useState } from "react";
import toast from "react-hot-toast";

interface Props {
  request: MaterialRequest | null;
  accessToken: string;
}

function RequestDetails({ request, accessToken }: Props) {
  if (!request) {
    return <div>Select a request</div>;
  }

  const handleApprove = async () => {
    try {
      await approveRequest(accessToken, request.mrf_id);
    } catch (error) {
      console.error(error);
    } finally {
      toast.success("Approved");
    }
  };
  const handleDispprove = async () => {
    try {
      await disapproveRequest(accessToken, request.mrf_id);
    } catch (error) {
      console.error(error);
    } finally {
      toast.success("Dispproved");
    }
  };

  return (
    <div className="ring ring-gray-400 p-4 flex flex-col rounded-lg">
      <h2 className="text-xl font-semibold">MRF-{request.mrf_id}</h2>

      <div className="flex flex-row justify-between">
        <section>
          <p>
            Requested by: {request.requestor_email}
            <span></span>
          </p>
          <p>Approval Status: {request.approval_status}</p>
          {/* <p>{request.release_status}</p> */}

          <section>
            <h1 className="font-semibold">Items:</h1>

            <div>
              {request.items.map((item, index) => (
                <div key={index}>
                  Product {item.product_id}
                  {" - "}
                  Qty {item.quantity}
                </div>
              ))}
            </div>
          </section>
        </section>

        <section className="flex flex-row gap-3 h-10">
          <button
            onClick={handleApprove}
            className="size-15 bg-green-500 font-semibold text-white ring rounded-full"
            type="button"
          >
            Approve
          </button>
          <button
            onClick={handleDispprove}
            className="size-15 bg-red-500 font-semibold text-white ring rounded-full"
            type="button"
          >
            Disapprove
          </button>
        </section>
      </div>
    </div>
  );
}

export default RequestDetails;
