
import { MaterialRequest } from "@/src/types/materialRequest";
import React from "react";

import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import { Product } from "@/src/types/product";
import { Badge } from "@/components/ui/badge";

interface Props {
  requests: MaterialRequest[];
  products: Product[];
}

function Requests({ requests, products }: Props) {
  return (
    <div className="flex flex-col gap-3">
      <h1 className="text-lg">My Requests</h1>

      {requests.map((req) => {
        let statusText = "";

        if (req.approval_status === "Pending") {
          statusText = "For Approval";
        } else if (req.approval_status === "Approved") {
          statusText = "For Release";
        } else if (req.approval_status === "Not Approved") {
          statusText = "Not Approved";
        }

        if (req.approval_status === "Approved" && req.release_status === "Pending") {
          statusText = "For Release";
        } else if (req.approval_status === "Approved"  && req.release_status === "Released") {
          statusText = "Released";
        } else if (req.approval_status === "Approved" && req.release_status === "Not Released") {
          statusText = "Rejected";
        }

         const getBadgeClass = (statusText: string) => {
            switch (statusText) {
            case "For Approval":
                return "bg-yellow-500 hover:bg-yellow-600 text-white";
            case "Approved":
                return "bg-green-500 hover:bg-green-600 text-white";
            case "Not Approved":
                return "bg-red-500 hover:bg-red-600 text-white";
            case "For Release":
                return "bg-amber-500 hover:bg-green-600 text-white";
            case "Released":
                return "bg-green-500 hover:bg-green-600 text-white";
            case "Rejected":
                return "bg-red-500 hover:bg-green-600 text-white";
            default:
                return "bg-gray-500 text-white";
            }
        };

        return (
          <Card key={req.mrf_id}>
            <CardHeader>
              <CardTitle>
                {new Date(req.date).toLocaleDateString("en-US", {
                    year: "numeric",
                    month: "long",
                    day: "numeric"
                })}
              </CardTitle>

              <CardDescription>
                MRF #{req.mrf_id}
              </CardDescription>

              <CardAction>
                <Badge className={getBadgeClass(statusText)}>
                    {statusText}
                </Badge>
              </CardAction>
            </CardHeader>

            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Product</TableHead>
                    <TableHead>Quantity</TableHead>
                  </TableRow>
                </TableHeader>

                <TableBody>
                  {req.items.map((item) => {
                    const product = products.find(
                      (product) => product.id === item.product_id
                    );

                    return (
                      <TableRow key={item.product_id}>
                        <TableCell>
                          {product?.product_name ?? `Product ${item.product_id}`}
                        </TableCell>

                        <TableCell>
                          {item.quantity}
                        </TableCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}

export default Requests;
