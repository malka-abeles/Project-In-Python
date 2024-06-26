from services import VisualizationService
from fastapi import APIRouter, Request, HTTPException
from utils.log import log


visualization_router = APIRouter()


@visualization_router.get("/monthlyBudget/{user_id}/{month}")
@log
async def month_budget(request: Request, user_id: int, month: str):
    return await VisualizationService.get_expenses_against_revenues_by_month(user_id, month)


@visualization_router.get("/monthlyBudget/{user_id}/{month}")
@log
async def month_budget(request: Request, user_id: int, month: str):
    return await VisualizationService.get_expenses_against_revenues_by_month(user_id, month)


@visualization_router.get("/yearlyExpensesVsRevenuesBar/{user_id}")
@log
async def year_divide_to_months_budget(request: Request, user_id: int):
    return await VisualizationService.get_expenses_against_revenues_by_month_all_year(user_id)


@visualization_router.get("/yearlyExpensesVsRevenuesGraph/{user_id}")
@log
async def yearly_graph(request: Request, user_id: int):
    return await VisualizationService.get_yearly_graph(user_id)


@visualization_router.get("/yearlyBalanceGraph/{user_id}")
@log
async def yearly_balance_graph(request: Request, user_id: int):
    return await VisualizationService.get_balances_yearly_graph(user_id)


@visualization_router.get("/yearlyBalanceBar/{user_id}")
@log
async def yearly_balance_bar(request: Request, user_id: int):
    return await VisualizationService.get_balance_yearly_bar(user_id)