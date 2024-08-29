// Sidebar imports
import {
  UilEstate,
  UilClipboardAlt,
  UilUsersAlt,
  UilPackage,
  UilChart,
  UilSignOutAlt,
} from "@iconscout/react-unicons";

// Analytics Cards imports
import { UilUsdSquare, UilMoneyWithdrawal } from "@iconscout/react-unicons";
import { keyboard } from "@testing-library/user-event/dist/keyboard";

// Recent Card Imports
import img1 from "../imgs/img1.png";
import profile from "../imgs/profile.png"
import img3 from "../imgs/img3.png";

// Sidebar Data
export const SidebarData = [
  {
    icon: UilEstate,
    heading: "Painel",
  },
  {
    icon: UilClipboardAlt,
    heading: "Pedidos",
  },
  {
    icon: UilUsersAlt,
    heading: "Clientes",
  },
  {
    icon: UilPackage,
    heading: 'Produtos'
  },
  {
    icon: UilChart,
    heading: 'Análises'
  },
];

// Analytics Cards Data
export const cardsData = [
  {
    title: "Vendas",
    color: {
      backGround: "linear-gradient(180deg, #bb67ff 0%, #c484f3 100%)",
      boxShadow: "0px 10px 20px 0px #e0c6f5",
    },
    barValue: 70,
    value: "25,970",
    png: UilUsdSquare,
    series: [
      {
        name: "Vendas",
        data: [23.87, 30.8, 21.56, 39.27, 32.34, 84.03, 77],
      },
    ],
  },
  {
    title: "Faturamento",
    color: {
      backGround: "linear-gradient(180deg, #FF919D 0%, #FC929D 100%)",
      boxShadow: "0px 10px 20px 0px #FDC0C7",
    },
    barValue: 50,
    value: "12,345",
    png: UilMoneyWithdrawal,
    series: [
      {
        name: "Faturamento",
        data: [7.7, 77, 38.5, 53.9, 61.6, 23.1, 30.8],
      },
    ],
  },
  {
    title: "Custos",
    color: {
      backGround:
        "linear-gradient(rgb(248, 212, 154) -146.42%, rgb(255 202 113) -46.42%)",
      boxShadow: "0px 10px 20px 0px #F9D59B",
    },
    barValue: 60,
    value: "4,270",
    png: UilClipboardAlt,
    series: [
      {
        name: "Custos",
        data: [7.7, 19.25, 11.55, 23.1, 9.24, 11.55, 15.4],
      },
    ],
  },
];

// Recent Update Card Data
export const UpdatesData = [
  {
    img: img1,
    name: "Andrew Thomas",
    noti: "encomendou um smartwatch da Apple com bateria de 2500mAh.",
    time: "25 segundos atrás",
  },
  {
    img: profile,
    name: "James Bond",
    noti: "recebeu um gadget da Samsung para carregar a bateria.",
    time: "30 minutos atrás",
  },
  {
    img: img3,
    name: "Iron Man",
    noti: "encomendou um smartwatch da Apple e uma bateria de 2500mAh para o Samsung Gear.",
    time: "2 horas atrás",
  },
];
