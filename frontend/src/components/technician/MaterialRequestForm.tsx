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
    <form onSubmit={handleSubmit} className="grid grid-cols-1 gap-3">
      <div className="relative flex flex-col">
        <label htmlFor="">Product</label>
        <input type="text" 
                value={search}
                onChange={(e) => {
                    setSearch(e.target.value);
                    setSelectedProduct(null)
                }}
                placeholder="search here"
                className="ring ring-gray-400 px-2 rounded-md"
                
        />

        {search && !selectedProduct && (
            <div className="absolute top-11 w-full bg-white flex flex-col ring-1 rounded-md mt-2">
                {filteredProducts.map((product)=>(
                    <button
                        type="button"
                        key={product.id}
                        onClick={()=>{
                            setSelectedProduct(product);
                            setSearch(product.product_name)
                        }}
                        className="text-left px-2"
                    >
                        {product.product_name}
                    </button>
                ))}

            </div>
        )}
      </div>

      <div className="flex flex-col">
        <label>Quantity</label>

        <input
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(e.target.value)}
          className="ring ring-gray-400 px-2 rounded-md"
        />

        <button className="mt-3 ring-2 ring-blue-600 text-blue-700 rounded-md" type="button" onClick={handleAddItem}>
            Add Item
        </button>
      </div>

      

      <div>


    <div className="flex flex-row justify-between">
        <h3>Items for Request <span>{items.length}</span></h3>

        {items.length > 0 ? 
        <button onClick={()=>{setItems([])}}>Reset</button>: "No Items"}
    </div>


    <section>

    {items.map((item, index) => {
        const product = products.find(
        (product) => product.id === item.product_id
        );

        return (

        <div className="grid grid-cols-2" key={index}>
            <span>
            {product?.product_name}
            </span>

            <span>
            {item.quantity}
            </span>
        
        </div>


        );
    })}
    
    </section>
    </div>

    <section className="flex flex-col gap-2">
      
      <button className="ring-2 bg-blue-600 text-white rounded-md" type="submit">
        Submit MRF
      </button>
    </section>
    </form>
  )
}

export default MaterialRequestForm
