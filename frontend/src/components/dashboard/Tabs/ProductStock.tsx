"use client";

import { getTotalProductsStock } from "@/src/services/inventoryService";
import { ProductStockByArea } from "@/src/types/inventory";
import { Product } from "@/src/types/product";
import React, { useState } from "react";

import { Button } from "@/components/ui/button";

import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from "@/components/ui/combobox";

import {
  Table,
  TableBody,
  TableCell,
  TableRow,
} from "@/components/ui/table";

interface Props {
  products: Product[];
  accessToken: string;
}

function ProductStockView({ products, accessToken }: Props) {
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [productStock, setProductStock] = useState<ProductStockByArea | null>(null);

  const handleViewStock = async () => {
    if (!selectedProduct) return;

    try {
      const data = await getTotalProductsStock(accessToken, selectedProduct.id);
      setProductStock(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <div>
        <section className="grid grid-cols-2 gap-3">
          <Combobox
            items={products}
            value={selectedProduct}
            onValueChange={(product: Product | null) => setSelectedProduct(product)}
          >
            <ComboboxInput
              placeholder="Select a product"
              value={selectedProduct ? selectedProduct.product_name : ""}
            />
            <ComboboxContent>
              <ComboboxEmpty>No products found.</ComboboxEmpty>
              <ComboboxList>
                {(product: Product) => (
                  <ComboboxItem key={product.id} value={product}>
                    {product.product_name}
                  </ComboboxItem>
                )}
              </ComboboxList>
            </ComboboxContent>
          </Combobox>

          <Button
            onClick={handleViewStock}
            disabled={!selectedProduct}
            variant="outline"
            className="bg-blue-500 rounded-md text-white font-bold disabled:bg-gray-600 cursor-pointer"
          >
            View Stock
          </Button>
        </section>

        {productStock && (
          <div className="mt-4">
            <Table>
              <TableBody>
                {productStock.areas.map((area) => (
                  <TableRow key={area.area} className="text-center">
                    <TableCell className="font-medium">{area.area}</TableCell>
                    <TableCell>{area.stock}</TableCell>
                    <TableCell>
                      <Button variant="outline" className="cursor-pointer">
                        Add Stock
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProductStockView;