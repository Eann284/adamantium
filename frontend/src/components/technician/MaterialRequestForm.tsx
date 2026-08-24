"use client";

import { createMaterialRequest } from "@/src/services/requestService";
import { Product } from "@/src/types/product";
import type { MRFItem } from "@/src/types/materialRequest";

import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

import React, { useState } from "react";
import { Icon, IterationCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Props {
  accessToken: string;
  products: Product[];
}

function MaterialRequestForm({ accessToken, products }: Props) {
  const [search, setSearch] = useState("");
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [quantity, setQuantity] = useState("");
  const [items, setItems] = useState<MRFItem[]>([]);

  const filteredProducts = products.filter((product) =>
    product.product_name.toLowerCase().includes(search.toLowerCase()),
  );

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    console.log("SUBMIT CLICKED");
    console.log("ITEMS:", items);
    console.log("ACCESS TOKEN:", accessToken);

    if (items.length === 0) {
      console.log("NO ITEMS");
      return;
    }

    const data = {
      items,
      mrf_files: null,
    };

    console.log("DATA TO SEND:", data);

    try {
      console.log("CALLING createMaterialRequest...");

      const result = await createMaterialRequest(accessToken, data);

      console.log("MRF created:", result);
    } catch (error) {
      console.error("MRF ERROR:", error);
    }
  };

  const handleAddItem = () => {
    if (!selectedProduct || !quantity) {
      return;
    }

    const newItem: MRFItem = {
      product_id: selectedProduct.id,
      quantity: Number(quantity),
    };

    setItems((previous) => [...previous, newItem]);

    setSelectedProduct(null);
    setSearch("");
    setQuantity("");
  };

  return (
    <form onSubmit={handleSubmit} >

    <h1 className="mb-3 text-lg">Material Request Form</h1>
        <main className="grid grid-cols-2 gap-5">

      <div className="border border-gray-200 p-2 flex flex-col gap-3 rounded-lg">
        <h1 className="border-b-2">Select Products to Request</h1>
        <div className="relative flex flex-col gap-1">
          <label htmlFor="">Product</label>
          <Input
            type="text"
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setSelectedProduct(null);
            }}
            placeholder="search here"
            className="ring ring-gray-200 px-2 rounded-md"
          />

          {search && !selectedProduct && (
            <div className="absolute top-15 w-full bg-white flex flex-col ring- mt-2">
              {filteredProducts.map((product) => (
                <Button
                  type="button"
                  key={product.id}
                  onClick={() => {
                    setSelectedProduct(product);
                    setSearch(product.product_name);
                  }}
                  className="text-left px-2 rounded-none"
                  variant="outline"
                >
                  {product.product_name}
                </Button>
              ))}
            </div>
          )}
        </div>

        <div className="flex flex-col gap-1">
          <label>Quantity</label>

          <Input
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="ring ring-gray-200 px-2 rounded-md"
          />

          <Button
            className="mt-3 bg-blue-500 text-white font-semibold rounded-md"
            type="button"
            onClick={handleAddItem}
          >
            Add Item
          </Button>
        </div>
      </div>

      <div>
        <div className="border border-gray-200 p-2 h-full rounded-lg">
          <div className="flex flex-row items-center justify-between border-b-2">
            <h3>
              Items for Request <span>{items.length}</span>
            </h3>

            {items.length > 0 ? (
        
              <Button onClick={() => {
                  setItems([]);
                }} className="rounded-sm py-0 w-20 h-7 bg-blue-500 text-white font-semibold">
                Reset

              </Button>
            ) : (
              ""
            )}
          </div>

          <div className="h-full overflow-y-auto">
            {items.length <= 0 ? (
             <div className="p-2 h-full flex flex-col justify-center items-center">
                <h1 className="text-center font-light">No Items</h1>
             </div>
            ) : (
              items.map((item, index) => {
                const product = products.find(
                  (product) => product.id === item.product_id,
                );

                return (
                
                  <Table key={index} className="table-fixed">
                    <TableBody>
                        <TableRow>
                        <TableCell className="font-medium">{product?.product_name}</TableCell>
                        <TableCell>Quantity: {item.quantity}</TableCell>
                        </TableRow>
                    </TableBody>
                    </Table>
                );
              })
            )}
          </div>
        </div>
      </div>

        </main>
      <section className="flex flex-col gap-2 mt-2">
        <Button
          className="ring-2 bg-blue-600 text-white rounded-md"
          type="submit"
        >
          Submit MRF
        </Button>
      </section>

    </form>
  );
}

export default MaterialRequestForm;
