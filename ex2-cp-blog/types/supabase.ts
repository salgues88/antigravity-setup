export type Category = {
    id: string;
    name: string;
    created_at: string;
};

export type Post = {
    id: string;
    title: string;
    summary: string | null;
    content: string;
    image_url: string | null;
    category_id: string | null;
    author_id: string | null;
    created_at: string;
    updated_at: string;
};
