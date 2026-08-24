"use client";
import {
  approveRequest,
  disapproveRequest,
} from "@/src/services/requestService";
import { MaterialRequest } from "@/src/types/materialRequest";
import toast from "react-hot-toast";

import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyMedia,
  EmptyTitle,
} from "@/components/ui/empty";

import { Product } from "@/src/types/product";

interface Props {
  request: MaterialRequest | null;
  products: Product[];
  accessToken: string;
}

function RequestDetails({ request, products, accessToken }: Props) {
  if (!request) {
    return (
      <Empty>
        <EmptyHeader>
          <EmptyTitle>No Request Selected.</EmptyTitle>
          <EmptyDescription>Please Select a Request to view.</EmptyDescription>
        </EmptyHeader>
      </Empty>
    );
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
  const handleDisapprove = async () => {
    try {
      await disapproveRequest(accessToken, request.mrf_id);
    } catch (error) {
      console.error(error);
    } finally {
      toast.success("Dispproved");
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>
          <h1 className="text-xl font-semibold">MRF - {request.mrf_id}</h1>
        </CardTitle>
        <CardDescription>
          Requested by: {request.requestor_email}
        </CardDescription>
        <CardAction className="flex flex-col"></CardAction>
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
            {request.items.map((item) => {
              const product = products.find(
                (product) => product.id === item.product_id,
              );

              return (
                <TableRow key={item.product_id}>
                  <TableCell>
                    {product?.product_name ?? `Product ${item.product_id}`}
                  </TableCell>

                  <TableCell>{item.quantity}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </CardContent>
      <CardFooter className="flex flex-row gap-2">
        <Button className="bg-green-500" onClick={handleApprove}>
          Approve
        </Button>
        <Button className="bg-red-500" onClick={handleDisapprove}>
          Disapprove
        </Button>
      </CardFooter>
    </Card>
  );
}

export default RequestDetails;
