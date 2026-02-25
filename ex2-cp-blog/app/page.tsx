"use client";

import { useEffect, useState } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import CategoryFilter from "@/components/CategoryFilter";
import PostCard from "@/components/PostCard";
import Pagination from "@/components/Pagination";
import { createClient } from "@/lib/supabase/client";
import { Category, Post } from "@/types/supabase";
import { User } from "@supabase/supabase-js";

const POSTS_PER_PAGE = 6;

export default function Home() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [posts, setPosts] = useState<Post[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPosts, setTotalPosts] = useState(0);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);

  const supabase = createClient();

  useEffect(() => {
    async function getUser() {
      const { data: { user } } = await supabase.auth.getUser();
      setUser(user);
    }
    getUser();
  }, [supabase]);

  useEffect(() => {
    async function fetchCategories() {
      const { data } = await supabase
        .from("categories")
        .select("*")
        .order("name");
      if (data) setCategories(data);
    }
    fetchCategories();
  }, [supabase]);

  useEffect(() => {
    async function fetchPosts() {
      setLoading(true);
      let query = supabase
        .from("posts")
        .select("*", { count: "exact" })
        .order("created_at", { ascending: false });

      if (selectedCategory) {
        query = query.eq("category_id", selectedCategory);
      }

      // Pagination setup
      const from = (currentPage - 1) * POSTS_PER_PAGE;
      const to = from + POSTS_PER_PAGE - 1;
      query = query.range(from, to);

      const { data, count } = await query;

      if (data) setPosts(data);
      if (count !== null) setTotalPosts(count);

      setLoading(false);
    }

    fetchPosts();
  }, [supabase, selectedCategory, currentPage]);

  const handleCategoryChange = (categoryId: string | null) => {
    setSelectedCategory(categoryId);
    setCurrentPage(1); // Reset to first page when changing category
  };

  const totalPages = Math.ceil(totalPosts / POSTS_PER_PAGE);

  return (
    <div className="flex min-h-screen flex-col bg-gray-50 text-black">
      <Header user={user} />

      <main className="flex-1">
        {/* Hero Section */}
        <section className="bg-white py-20 border-b border-gray-200">
          <div className="mx-auto max-w-5xl px-4 text-center sm:px-6 lg:px-8">
            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl text-black">
              Welcome to <span className="text-blue-600">Antigravity</span> blog
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-500">
              Here you can find the latest articles about web development, Next.js,
              Supabase, Tailwind CSS, and more.
            </p>
          </div>
        </section>

        {/* Content Section */}
        <section className="mx-auto max-w-5xl px-4 py-12 sm:px-6 lg:px-8">
          <CategoryFilter
            categories={categories}
            selectedCategoryId={selectedCategory}
            onSelectCategory={handleCategoryChange}
          />

          {loading ? (
            <div className="flex h-64 items-center justify-center">
              <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
            </div>
          ) : (
            <>
              {posts.length > 0 ? (
                <>
                  <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
                    {posts.map((post) => {
                      const category = categories.find((c) => c.id === post.category_id);
                      return (
                        <PostCard
                          key={post.id}
                          post={post}
                          categoryName={category?.name}
                        />
                      );
                    })}
                  </div>
                  <Pagination
                    currentPage={currentPage}
                    totalPages={totalPages}
                    onPageChange={setCurrentPage}
                  />
                </>
              ) : (
                <div className="flex h-40 flex-col items-center justify-center rounded-2xl border border-dashed border-gray-300 bg-white">
                  <p className="text-gray-500">No posts found in this category.</p>
                </div>
              )}
            </>
          )}
        </section>
      </main>

      <Footer />
    </div>
  );
}
