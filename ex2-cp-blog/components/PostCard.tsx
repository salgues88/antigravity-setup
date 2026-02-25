import Image from "next/image";
import Link from "next/link";
import { Post, Category } from "@/types/supabase";

type PostCardProps = {
    post: Post;
    categoryName?: string;
};

export default function PostCard({ post, categoryName }: PostCardProps) {
    const formattedDate = new Date(post.created_at).toLocaleDateString("ko-KR", {
        year: "numeric",
        month: "long",
        day: "numeric",
    });

    return (
        <Link
            href={`/posts/${post.id}`}
            className="group flex flex-col overflow-hidden rounded-2xl border border-gray-200 bg-white transition-all hover:shadow-md"
        >
            <div className="relative h-48 w-full overflow-hidden bg-gray-100 sm:h-56">
                {post.image_url ? (
                    <Image
                        src={post.image_url as string}
                        alt={post.title}
                        fill
                        className="object-cover transition-transform duration-300 group-hover:scale-105"
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                    />
                ) : (
                    <div className="flex h-full w-full items-center justify-center bg-gray-200 text-gray-400">
                        No Image
                    </div>
                )}
            </div>
            <div className="flex flex-1 flex-col p-5">
                <div className="mb-2 flex items-center justify-between">
                    <span className="inline-flex items-center rounded-full bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-700">
                        {categoryName || "Uncategorized"}
                    </span>
                    <span className="text-xs text-gray-500">{formattedDate}</span>
                </div>
                <h3 className="mb-2 text-xl font-bold tracking-tight text-gray-900 group-hover:text-blue-600">
                    {post.title}
                </h3>
                <p className="line-clamp-2 flex-1 text-sm text-gray-600">
                    {post.summary || post.content.substring(0, 100) + "..."}
                </p>
            </div>
        </Link>
    );
}
