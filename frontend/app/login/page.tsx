"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { signIn } from "next-auth/react";
import { useForm } from "react-hook-form";
import toast from "react-hot-toast";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface Login {
  email: string;
  password: string;
}

function LoginPage() {
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<Login>();

  const onSubmit = async (data: Login) => {
    setLoading(true);
    try {
      const result = await signIn("credentials", {
        email: data.email,
        password: data.password,
        redirect: false,
      });

      if (result?.error) {
        toast.error("Invalid email or password");
      } else {
        toast.success("Logged in");
        router.push("/dashboard");
      }
    } catch (error) {
      toast.error("Error");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex flex-1 h-screen items-center justify-center p-4 gap-2">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle>
            <h1 className="font-semibold text-lg">Inventory Management System</h1>
          </CardTitle>
          <CardDescription>Please Log in to continue.</CardDescription>
        </CardHeader>
          <form onSubmit={handleSubmit(onSubmit)}>
          <CardContent>
            <div>
              <section className="flex flex-col gap-1">
                <Label className="font-semibold">Email</Label>
                <Input
                  {...register("email", {
                    required: "Email is required",
                    pattern: {
                      value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                      message: "Invalid email address",
                    },
                  })}
                  type="email"
                  placeholder="Email"
                  className="rounded-lg"
                />
              </section>
              {errors.email && (
                <p className="text-red-500 text-sm mt-1 mb-1">
                  {errors.email.message}
                </p>
              )}

              <section className="flex flex-col gap-1 mt-2">
                <Label htmlFor="" className="font-semibold">
                  Password
                </Label>
                <Input
                  {...register("password", {
                    required: "Password is required",
                  })}
                  type="password"
                  placeholder="Password"
                  className="rounded-lg"
                />
              </section>
              {errors.password && (
                <p className="text-red-500 text-sm mt-1 mb-1">
                  {errors.password.message}
                </p>
              )}
            </div>
            </CardContent>
            <CardFooter className="border-t mt-2">
              <Button type="submit" className="w-full bg-blue-500 text-white font-semibold rounded-lg cursor-pointer mt-2">
                {loading ? "Logging in..." : "Log In"}
              </Button>
            </CardFooter>
          </form>
      </Card>
    </main>
  );
}

export default LoginPage;
