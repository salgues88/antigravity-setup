import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import WriteForm from "./WriteForm";

// Force dynamic rendering since we read cookies inside the page
export const dynamic = "force-dynamic";

export default async function WritePage() {
    const supabase = await createClient();

    // Check if user is authenticated
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
        redirect("/login");
    }

    // Fetch existing categories for the dropdown
    const { data: categories } = await supabase
        .from("categories")
        .select("*")
        .order("name");

    return (
        <div className="flex min-h-screen flex-col bg-gray-50 text-black">
            <Header user={user} />

            <main className="flex-1 py-12 px-4 sm:px-6 lg:px-8">
                <div className="max-w-4xl mx-auto bg-white p-8 rounded-2xl shadow-sm border border-gray-100">
                    <h1 className="text-3xl font-extrabold text-gray-900 mb-2">Write a new post</h1>
                    <p className="text-gray-500 mb-2">Draft your thoughts using Markdown and share them with the world.</p>

                    <WriteForm categories={categories || []} />
                </div>
            </main>

            <Footer />
        </div>
    );
}
