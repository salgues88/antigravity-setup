"use server";

import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

export async function publishPost(formData: FormData) {
    const supabase = await createClient();

    const { data: { user } } = await supabase.auth.getUser();
    if (!user) {
        throw new Error("Unauthorized");
    }

    const title = formData.get("title") as string;
    const category_id = formData.get("category_id") as string;
    const content = formData.get("content") as string;

    if (!title || !content) {
        throw new Error("Title and content are required");
    }

    const { data: post, error } = await supabase.from("posts").insert({
        title,
        category_id: category_id || null,
        content,
        author_id: user.id
    }).select().single();

    if (error || !post) {
        throw new Error("Failed to publish post: " + error?.message);
    }

    redirect(`/posts/${post.id}`);
}
