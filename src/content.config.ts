import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishDate: z.coerce.date(),
    category: z.string(),
    tags: z.array(z.string()).optional(),
    heroImage: z.string().optional(),
    featured: z.boolean().optional().default(false),
    affiliate: z.object({
      enabled: z.boolean().optional().default(false),
      products: z.array(z.object({
        name: z.string(),
        points: z.array(z.string()).optional(),
        target: z.string().optional(),
        rakutenUrl: z.string().optional(),
        roomUrl: z.string().optional(),
      })).optional(),
    }).optional(),
  }),
});

export const collections = { blog };
