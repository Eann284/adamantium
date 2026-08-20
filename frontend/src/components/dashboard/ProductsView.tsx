import React from "react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import AllProducts from "./Tabs/AllProducts";
import { Product } from "@/src/types/product";
import ProductStockView from "./Tabs/ProductStock";

interface Props {
  products: Product[];
  accessToken: string
}
function ProductsView({products, accessToken}:Props) {
  return (
    <Tabs defaultValue="account" className="w-[400px]">
      <TabsList>
        <TabsTrigger value="account">Products</TabsTrigger>
        <TabsTrigger value="password">Product Stock</TabsTrigger>
      </TabsList>
      <TabsContent value="account">
        <AllProducts products={products}/>
      </TabsContent>
      <TabsContent value="password">
        <ProductStockView products={products} accessToken={accessToken}/>
      </TabsContent>
    </Tabs>
  );
}

export default ProductsView;
