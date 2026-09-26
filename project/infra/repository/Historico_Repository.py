from __future__ import annotations

from decimal import Decimal
from typing import Iterable

from project.domain.ProdutoCarrinho import ProdutoCarrinho
from project.infra.configs.connection import DBConnectionHandler
from project.infra.entities.historico_compra import (
    Historico_Compra as Historico_Entity,
)
from project.infra.entities.item_historico_compra import (
    Item_Historico_Compra as Item_Entity,
)
from project.infra import entities as _entities


class Historico_Compra_Repository:

    @staticmethod
    def registrar_compra(
        id_cli: int,
        valor_total: Decimal,
        itens_carrinho: Iterable[ProdutoCarrinho],
    ) -> bool:

        if not isinstance(id_cli, int) or id_cli < 1:
            return False

        if not isinstance(valor_total, Decimal) or valor_total < 0:
            return False

        itens = list(itens_carrinho)

        if not itens:
            return False

        # Validação dos itens
        for item in itens:

            if not isinstance(item, ProdutoCarrinho):
                return False

            # O produto precisa já existir no banco
            # para que o id_prod possa ser gravado.
            if item.produto.id_prod is None:
                return False

        # Recalcula o valor da compra para evitar
        # registrar um valor_total incorreto.
        valor_calculado = sum(
            (
                item.produto.preco * item.quantidade
                for item in itens
            ),
            Decimal("0.00"),
        )

        if valor_calculado != valor_total:
            raise ValueError(
                "O valor_total informado não corresponde "
                "ao total dos itens da compra."
            )

        with DBConnectionHandler() as db:

            # Cabeçalho da compra
            historico_entity = Historico_Entity(
                id_cli=id_cli,
                valor_total=valor_total,
            )

            # Itens da compra
            for item in itens:

                item_entity = Item_Entity(
                    id_prod=item.produto.id_prod,
                    quantidade=item.quantidade,
                    # IMPORTANTE:
                    # salva o preço daquele momento,
                    # e não o preço futuro do produto.
                    preco_momento=item.produto.preco,
                )

                historico_entity.itens.append(item_entity)

            db.session.add(historico_entity)

        return True

    @staticmethod
    def buscar_por_id(
        id_historico: int,
    ) -> dict | None:

        if not isinstance(id_historico, int) or id_historico < 1:
            return None

        with DBConnectionHandler() as db:

            historico = (
                db.session
                .query(Historico_Entity)
                .filter_by(id_historico=id_historico)
                .first()
            )

            if historico is None:
                return None

            return {
                "id_historico": historico.id_historico,
                "id_cli": historico.id_cli,
                "valor_total": historico.valor_total,
                "data_compra": historico.data_compra,
                "itens": [
                    {
                        "id_item": item.id_item,
                        "id_prod": item.id_prod,
                        "quantidade": item.quantidade,
                        "preco_momento": item.preco_momento,
                    }
                    for item in historico.itens
                ],
            }

    @staticmethod
    def listar_por_cliente(
        id_cli: int,
    ) -> list[dict]:

        if not isinstance(id_cli, int) or id_cli < 1:
            return []

        with DBConnectionHandler() as db:

            historicos = (
                db.session
                .query(Historico_Entity)
                .filter_by(id_cli=id_cli)
                .order_by(Historico_Entity.data_compra.desc())
                .all()
            )

            return [
                {
                    "id_historico": historico.id_historico,
                    "id_cli": historico.id_cli,
                    "valor_total": historico.valor_total,
                    "data_compra": historico.data_compra,
                    "itens": [
                        {
                            "id_item": item.id_item,
                            "id_prod": item.id_prod,
                            "quantidade": item.quantidade,
                            "preco_momento": item.preco_momento,
                        }
                        for item in historico.itens
                    ],
                }
                for historico in historicos
            ]