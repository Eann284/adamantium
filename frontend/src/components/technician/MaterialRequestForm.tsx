"use client";

import { createMaterialRequest } from "@/src/services/requestService";
import { Product } from "@/src/types/product";
import type { MRFItem } from "@/src/types/materialRequest";


import React, { useState } from "react";


interface Props {
   accessToken: string,
   products: Product[]
}

function MaterialRequestForm({accessToken, products}:Props) {

    const [search, setSearch] = useState("");
    const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
    const [quantity, setQuantity] = useState("");
    const [items, setItems] = useState<MRFItem[]>([]);
    
    const filteredProducts = products.filter(
        (product) => product.product_name.toLowerCase().includes(search.toLowerCase())
    );

    const handleSubmit = async (
        e: React.FormEvent<HTMLFormElement>
        ) => {
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

            const result = await createMaterialRequest(
                accessToken,
                data
            );

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
            quantity: Number(quantity)
        };

        setItems((previous)=>[
            ...previous,
            newItem,
        ]);

        setSelectedProduct(null);
        setSearch("");
        setQuantity("");
        
    }


  return (
    <form onSubmit={handleSubmit}>
      <div>

        <label htmlFor="">Product</label>
        <input type="text" 
                value={search}
                onChange={(e) => {
                    setSearch(e.target.value);
                    setSelectedProduct(null)
                }}
                placeholder="search here"
        />

        {search && !selectedProduct && (
            <div>
                {filteredProducts.map((product)=>(
                    <button
                        type="button"
                        key={product.id}
                        onClick={()=>{
                            setSelectedProduct(product);
                            setSearch(product.product_name)
                        }}
                    >
                        {product.product_name}
                    </button>
                ))}
            </div>
        )}


      </div>

      <div>
        <label>Quantity</label>

        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
        />
      </div>

      <div>
  <h3>Selected Items</h3>

    {items.map((item, index) => {
        const product = products.find(
        (product) => product.id === item.product_id
        );

        return (
        <div key={index}>
            <span>
            {product?.product_name}
            </span>

            <span>
            {item.quantity}
            </span>
        </div>
        );
    })}
    </div>

      <button type="button" onClick={handleAddItem}>
        Add Item
      </button>
      <button type="submit">
        Submit MRF
      </button>
    </form>
  )
}

export default MaterialRequestForm
