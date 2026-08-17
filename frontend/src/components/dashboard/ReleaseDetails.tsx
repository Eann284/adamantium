"use client";
import { approveRequest, disapproveRequest, rejectRequest, releaseRequest } from "@/src/services/requestService";
import { MaterialRequest } from "@/src/types/materialRequest";
import React, { useState } from "react";
import toast from "react-hot-toast";


interface Props {
  release: MaterialRequest | null;
  accessToken: string
}

function ReleaseDetails({ release, accessToken }: Props) {


    
  if (!release) {
    return <div>Select a request</div>;
  }


  const handleRelease = async() => {
    console.log("Release button clicked");
    try {
        await releaseRequest(
            accessToken,
            release.mrf_id
        );
    } catch (error) {
        console.error(error)
    } finally {
        toast.success('Released')
    }
}
  const handleReject = async() => {
    try {
        await rejectRequest(
            accessToken,
            release.mrf_id
        );
    } catch (error) {
        console.error(error)
    } finally {
        toast.success('Rejected')
    }
}



  return (
    <div className="ring ring-gray-400 p-4 flex flex-col grow rounded-lg">
        
    <h2 className="text-xl font-semibold">MRF-{release.mrf_id}</h2>

    <div className="flex flex-row justify-between">

    <section>

      <p>Requested by: {release.requestor_email}<span></span></p>
      <p>Approval Status: {release.approval_status}</p>
      {/* <p>{request.release_status}</p> */}

        <section>
        <h1 className="font-semibold">Items:</h1>

        <div>
        {release.items.map((item, index) => (
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
        <button onClick={handleRelease}className="size-15 bg-green-500 font-semibold text-white ring rounded-full"  type="button">Release</button>
        <button onClick={handleReject}className="size-15 bg-red-500 font-semibold text-white ring rounded-full"  type="button">Reject</button>
      </section>
    </div>

    </div>
  );
}

export default ReleaseDetails;
