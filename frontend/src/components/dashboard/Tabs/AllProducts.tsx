import { Product } from "@/src/types/product";
import React from "react";
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

interface Props {
  products: Product[];
}

function AllProducts({ products }: Props) {
  return (
    <div>
      {/* <div>
        {products.map((product) => (
          <div key={product.id}>{product.product_name}</div>
        ))}
      </div> */}

      <Table>
        {/* <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">Product</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Method</TableHead>
            <TableHead className="text-right">Amount</TableHead>
          </TableRow>
        </TableHeader> */}
        <TableBody>
          { products.map((product) => (
            <TableRow key={product.id}>
              <TableCell className="font-medium">{product.product_name}</TableCell>
              {/* <TableCell>Paid</TableCell>
              <TableCell>Credit Card</TableCell>
              <TableCell className="text-right">$250.00</TableCell> */}
          </TableRow>
            ))
          }
        </TableBody>
      </Table>
    </div>
  );
}

export default AllProducts;
