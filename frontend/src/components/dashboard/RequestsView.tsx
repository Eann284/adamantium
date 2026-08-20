import React from "react";
import { MaterialRequest } from "@/src/types/materialRequest";
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
interface Props {
  requests: MaterialRequest[];
}

function RequestsView({ requests }: Props) {
  const getBadgeClass = (status: string) => {
    switch (status.toLowerCase()) {
      case "pending":
        return "bg-yellow-500 hover:bg-yellow-600 text-white";
      case "approved":
        return "bg-green-500 hover:bg-green-600 text-white";
      case "not approved":
        return "bg-red-500 hover:bg-red-600 text-white";
      default:
        return "bg-gray-500 text-white";
    }
  };

  const getReleaseBadgeClass = (status: string) => {
    switch (status.toLowerCase()) {
      case "pending":
        return "bg-yellow-500 hover:bg-yellow-600 text-white";
      case "released":
        return "bg-green-500 hover:bg-green-600 text-white";
      case "not released":
        return "bg-red-500 hover:bg-red-600 text-white";
      default:
        return "bg-gray-500 text-white";
    }
  };

  return (
    <div className="flex flex-col gap-2">
      {requests.map((req) => (
        // <div key={req.mrf_id} className='ring ring-gray-400 rounded-lg p-2'>
        //     <h1>{req.requestor_email}</h1>
        //     <h1>{req.release_status}</h1>
        // </div>

        <Card key={req.mrf_id}>
          <CardHeader>
            <CardTitle>
              <h1 className="text-xl font-semibold">MRF - {req.mrf_id}</h1>
            </CardTitle>
            <CardDescription>{req.requestor_email}</CardDescription>
            <CardAction>
              <Badge variant="default">{req.date}</Badge>
            </CardAction>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-[auto_1fr] gap-3">
              <h1>Approval Status</h1>
              <Badge className={getBadgeClass(req.approval_status)}>
                {req.approval_status}
              </Badge>

              <h1>Release Status</h1>
              <Badge className={getReleaseBadgeClass(req.release_status)}>
                {req.release_status}
              </Badge>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

export default RequestsView;
