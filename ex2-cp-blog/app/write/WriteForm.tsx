"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { publishPost } from "./actions";
import { Category } from "@/types/supabase";

// Import md-editor dynamically to prevent SSR errors
const MDEditor = dynamic(
    () => import("@uiw/react-md-editor"),
    { ssr: false }
);

export default function WriteForm({ categories }: { categories: Category[] }) {
    const [title, setTitle] = useState("");
    const [categoryId, setCategoryId] = useState("");
    const [content, setContent] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const formData = new FormData();
            formData.append("title", title);
            formData.append("category_id", categoryId);
            formData.append("content", content);

            // call server action
            await publishPost(formData);
        } catch (error) {
            console.error("Failed to publish:", error);
            alert("Failed to publish post. Please try again.");
            setLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-6 w-full mt-8">
            <div className="flex flex-col gap-2">
                <label htmlFor="title" className="text-sm font-medium text-gray-700">Title</label>
                <input
                    id="title"
                    type="text"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    required
                    className="border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900"
                    placeholder="Enter blog post title"
                />
            </div>

            <div className="flex flex-col gap-2">
                <label htmlFor="category" className="text-sm font-medium text-gray-700">Category</label>
                <select
                    id="category"
                    value={categoryId}
                    onChange={(e) => setCategoryId(e.target.value)}
                    className="border border-gray-300 rounded-lg p-3 outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-900 bg-white"
                >
                    <option value="">Select a category (optional)</option>
                    {categories.map((cat) => (
                        <option key={cat.id} value={cat.id}>
                            {cat.name}
                        </option>
                    ))}
                </select>
            </div>

            <div className="flex flex-col gap-2" data-color-mode="light">
                <label className="text-sm font-medium text-gray-700">Content</label>
                <div className="border border-gray-300 rounded-lg overflow-hidden">
                    <MDEditor
                        value={content}
                        onChange={(val) => setContent(val || "")}
                        height={500}
                        preview="edit"
                        className="w-full !border-0"
                    />
                </div>
            </div>

            <div className="flex justify-end mt-4">
                <button
                    type="submit"
                    disabled={loading || !title || !content}
                    className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg shadow-sm transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                    {loading ? "Publishing..." : "Publish post"}
                </button>
            </div>
        </form>
    );
}
