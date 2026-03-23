const Livre = {
    titre: "Jesus mon Prince",
    auteur: "twenty",
    anéée : 2026,
    prix: 2250,
    est_disponible: true
}
const produit = [
    {nom:"Riz",prix: 2500, quantite:10},
    {nom:"Tomate",prix: 7500, quantite:5},
    {nom:"Huile",prix: 1500, quantite:100},
    {nom:"Lait",prix: 700, quantite:24},
];

produit.forEach(produit =>{
    const totalProduit = produit.prix*produit.quantite;
    console.log(`Produit : ${ produit.nom}: ${totalProduit} `);
})