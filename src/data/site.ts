/**
 * Single source of truth for every string on the page.
 *
 * Prices are stored as numbers and formatted through `formatPrice()` so the
 * whole site can switch currency by editing one line.
 */

/* -------------------------------------------------------------------------- */
/* currency                                                                    */
/* -------------------------------------------------------------------------- */

const CURRENCY = 'USD';
const LOCALE = 'en-US';

const priceFormatter = new Intl.NumberFormat(LOCALE, {
  style: 'currency',
  currency: CURRENCY,
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

/** `2.5` -> `"$2.50"` */
export function formatPrice(value: number): string {
  return priceFormatter.format(value);
}

/* -------------------------------------------------------------------------- */
/* types                                                                       */
/* -------------------------------------------------------------------------- */

export interface NavLink {
  readonly label: string;
  readonly href: string;
  /** Renders the active underline. */
  readonly current?: boolean;
}

export type CardTone = 'glass' | 'cream';

export interface Product {
  readonly id: string;
  readonly name: string;
  readonly desc: string;
  readonly price: number;
  /** File name inside `src/assets/cups/`. */
  readonly img: string;
  /** Which `CupArt` variant to fall back to when the PNG is missing. */
  readonly art: 'heart' | 'rosetta' | 'bear' | 'leaf';
  readonly tone: CardTone;
  readonly alt: string;
}

export interface FooterColumn {
  readonly title: string;
  readonly items: readonly string[];
}

export interface PhoneNavItem {
  readonly icon: 'home' | 'cart' | 'user' | 'sliders';
  readonly label: string;
  readonly current?: boolean;
}

/* -------------------------------------------------------------------------- */
/* brand + meta                                                                */
/* -------------------------------------------------------------------------- */

export const site = {
  name: 'Flavored',
  tagline: 'Wake up to something special.',
  title: 'Flavored | Elegant Coffeehouse - Coffee The Best For You',
  description:
    'Flavored is an elegant coffeehouse. Coffee, the best for you — freshly roasted beans, lattes and a menu you can order from our app.',
  url: 'https://flavored.example.com',
  themeColor: '#2A0A0A',
  ogImageAlt: 'Flavored — an elegant coffeehouse',
  jsonLd: {
    '@context': 'https://schema.org',
    '@type': 'CafeOrCoffeeShop',
    name: 'Flavored',
    slogan: 'Wake up to something special.',
    url: 'https://flavored.example.com',
    servesCuisine: 'Coffee',
    priceRange: '$$',
  },
} as const;

/* -------------------------------------------------------------------------- */
/* navigation                                                                  */
/* -------------------------------------------------------------------------- */

export const navLinks: readonly NavLink[] = [
  { label: 'Home', href: '#home', current: true },
  { label: 'Coffee Menu', href: '#menu' },
  { label: 'About Us', href: '#about' },
  { label: 'Contact us', href: '#contact' },
];

export const navCta = { label: 'Coffee Shop', href: '#menu' } as const;

/* -------------------------------------------------------------------------- */
/* hero                                                                        */
/* -------------------------------------------------------------------------- */

export const hero = {
  heading: ['Coffee', 'The Best For You'],
  cta: { label: 'View Menu', href: '#menu' },
  chips: [
    { icon: 'cup-steam', label: 'Hot coffee', href: '#menu' },
    { icon: 'iced-glass', label: 'Iced coffee', href: '#menu' },
    { icon: 'takeaway-mug', label: 'Take-away', href: '#menu' },
    { icon: 'beans', label: 'Beans', href: '#menu' },
  ],
  cupAlt: 'Top-down latte with two cocoa-powder hearts in a white cup and saucer',
} as const;

/* -------------------------------------------------------------------------- */
/* products                                                                    */
/* -------------------------------------------------------------------------- */

export const products: readonly Product[] = [
  {
    id: 'americano',
    name: 'Americano',
    desc: '100% Natural Arabica or Robusta, 30 ml cup',
    price: 2.5,
    img: 'americano.png',
    art: 'rosetta',
    tone: 'glass',
    alt: 'Americano in a white cup with rosetta latte art',
  },
  {
    id: 'cappuccino',
    name: 'Cappuccino',
    desc: 'Coffee 50%, milk 50%, 280 ml',
    price: 2.5,
    img: 'cappuccino-bear.png',
    art: 'bear',
    tone: 'cream',
    alt: 'Cappuccino in a white cup with bear-face latte art',
  },
];

/** The wide translucent "Moccaccino" card on the left phone screen. */
export const moccaccino = {
  name: 'Moccaccino',
  desc: 'Mix with Coffee 30%, milk 50%, Water 20%, 280 ml + foam',
} as const;

/* -------------------------------------------------------------------------- */
/* product showcase (#menu)                                                    */
/* -------------------------------------------------------------------------- */

export const showcase = {
  heading: 'Lorem Ipsum is simply dummy text of',
  body: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,",
  cta: { label: 'Learn More', href: '#about' },
} as const;

/* -------------------------------------------------------------------------- */
/* feature spotlight (#about)                                                  */
/* -------------------------------------------------------------------------- */

export const feature = {
  heading: 'Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
  body: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
  cta: { label: 'Learn More', href: '#contact' },
  price: 2.5,
  cupAlt: 'Top-down latte with white tulip latte art surrounded by scattered coffee beans',
} as const;

/* -------------------------------------------------------------------------- */
/* app section                                                                 */
/* -------------------------------------------------------------------------- */

export const app = {
  heading: 'App is Available',
  body: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
  stores: [
    { icon: 'apple', label: 'Download on the App Store', href: '#' },
    { icon: 'google-play', label: 'Get it on Google Play', href: '#' },
  ],
  menuScreen: {
    title: 'Coffee',
    cta: 'View Menu',
    nav: [
      { icon: 'home', label: 'Home', current: true },
      { icon: 'cart', label: 'Cart' },
      { icon: 'user', label: 'Account' },
      { icon: 'sliders', label: 'Preferences' },
    ] as readonly PhoneNavItem[],
  },
  detailScreen: {
    title: 'Latte Grand',
    body: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
    priceLabel: 'Total Price',
    price: 3.5,
    addToCart: 'Add to Cart',
    cupAlt: 'Top-down latte with cocoa-powder heart art on a white saucer',
  },
} as const;

/* -------------------------------------------------------------------------- */
/* reserve CTA (#contact)                                                      */
/* -------------------------------------------------------------------------- */

export const reserve = {
  eyebrow: "Let's Talk",
  heading: 'Want to Reserve a Table?',
  cta: { label: 'Contact Now', href: '#contact' },
  body: "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
} as const;

/* -------------------------------------------------------------------------- */
/* footer                                                                      */
/* -------------------------------------------------------------------------- */

export const footerColumns: readonly FooterColumn[] = [
  { title: 'Our Services', items: ['Pricing', 'Tracking', 'Report a Bug', 'Terms of Services'] },
  { title: 'Our Company', items: ['Pricing', 'Tracking', 'Report a Bug', 'Terms of Services'] },
  { title: 'Address', items: ['Lorem Ipsum is', 'simply dummy', 'text of the', 'printing and'] },
];

export const skipLink = 'Skip to content' as const;
