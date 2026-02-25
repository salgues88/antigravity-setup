import Image from "next/image";
import { notFound } from "next/navigation";
import { createClient } from "@/lib/supabase/server";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import ShareButton from "@/components/ShareButton";

// Next.js 15+ async params requirement
type PageProps = {
    params: Promise<{ id: string }>;
};

export default async function PostPage({ params }: PageProps) {
    // Await the params before using them (Next.js 15+ requirement)
    const resolvedParams = await params;
    const postId = resolvedParams.id;

    const supabase = await createClient();

    // 1. Fetch user session for the Header
    const {
        data: { user },
    } = await supabase.auth.getUser();

    // 2. Fetch the specific post
    const { data: post, error } = await supabase
        .from("posts")
        .select(
            `
      *,
      category:categories(name)
    `
        )
        .eq("id", postId)
        .single();

    if (error || !post) {
        notFound();
    }

    const formattedDate = new Date(post.created_at).toLocaleDateString("ko-KR", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });

    // Since we don't have full profiles table yet, use a fallback for author
    const authorName = post.author_id ? "Authenticated User" : "Anonymous";

    return (
        <div className="flex min-h-screen flex-col bg-gray-50 text-black">
            <Header user={user} />

            <main className="flex-1 pb-20">
                {/* Article Header (Title, Meta, Share) */}
                <div className="mx-auto max-w-4xl px-4 pt-16 sm:px-6 lg:px-8">
                    <div className="mb-4 text-center">
                        {post.category && (
                            <span className="inline-block rounded-full bg-blue-100 px-3 py-1 text-sm font-semibold text-blue-800">
                                {post.category.name}
                            </span>
                        )}
                    </div>
                    <h1 className="mb-6 text-center text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl text-gray-900 leading-tight">
                        {post.title}
                    </h1>

                    {post.summary && (
                        <p className="mx-auto mb-8 max-w-2xl text-center text-xl text-gray-500">
                            {post.summary}
                        </p>
                    )}

                    <div className="flex flex-col items-center justify-between gap-4 border-y border-gray-200 py-6 sm:flex-row">
                        <div className="flex items-center gap-4">
                            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gray-200 text-xl font-bold text-gray-600">
                                {authorName.charAt(0)}
                            </div>
                            <div>
                                <p className="font-semibold text-gray-900">{authorName}</p>
                                <div className="flex items-center gap-2 text-sm text-gray-500">
                                    <span>{formattedDate}</span>
                                    <span>·</span>
                                    <span>5 min read</span>
                                </div>
                            </div>
                        </div>
                        <ShareButton />
                    </div>
                </div>

                {/* Thumbnail/Cover Image */}
                {post.image_url && (
                    <div className="mx-auto my-12 max-w-5xl px-4 sm:px-6 lg:px-8">
                        <div className="relative aspect-video w-full overflow-hidden rounded-2xl bg-gray-100 shadow-md">
                            <Image
                                src={post.image_url}
                                alt={post.title}
                                fill
                                priority
                                className="object-cover"
                                sizes="(max-width: 1200px) 100vw, 1200px"
                            />
                        </div>
                    </div>
                )}

                {/* Article Content */}
                <article className="mx-auto max-w-3xl px-4 sm:px-6 lg:px-8">
                    <div className="prose prose-lg prose-blue mx-auto mt-8 text-gray-800">
                        {/* If content is basic text, we use whitespace-pre-wrap to respect newlines. 
                If it was Markdown/HTML, we would use a different renderer. */}
                        <div className="whitespace-pre-wrap leading-relaxed">
                            {post.content}
                        </div>
                    </div>
                </article>
            </main>

            <Footer />
        </div>
    );
}
