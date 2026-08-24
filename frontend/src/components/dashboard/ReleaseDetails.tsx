"use client";
import { rejectRequest, releaseRequest } from "@/src/services/requestService";
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
  release: MaterialRequest | null;
  products: Product[]
  accessToken: string
}

function ReleaseDetails({ release, products, accessToken }: Props) {


    
  if (!release) {
    return (
      <Empty>
        <EmptyHeader>
          <EmptyTitle>No Request Selected.</EmptyTitle>
          <EmptyDescription>Please Select a Request to view.</EmptyDescription>
        </EmptyHeader>
      </Empty>
    );
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
    <Card>
      <CardHeader>
        <CardTitle>
          <h1 className="text-xl font-semibold">MRF - {release.mrf_id}</h1>
        </CardTitle>
        <CardDescription>
          Requested by: {release.requestor_email}
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
            {release.items.map((item) => {
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
        <Button className="bg-green-500" onClick={handleRelease}>
          Approve
        </Button>
        <Button className="bg-red-500" onClick={handleReject}>
          Disapprove
        </Button>
      </CardFooter>
    </Card>
  );
}

export default ReleaseDetails;
