"""
统一错误处理中间件
提供标准化的错误响应格式和日志记录
"""
import logging
import traceback
from pathlib import Path
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from typing import Union

# 确保logs目录存在
log_dir = Path('logs')
log_dir.mkdir(exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class ErrorResponse:
    """标准错误响应格式"""
    
    @staticmethod
    def format_error(
        error_code: str,
        message: str,
        details: Union[dict, list, str] = None,
        status_code: int = 500
    ) -> dict:
        """
        格式化错误响应
        
        Args:
            error_code: 错误代码
            message: 错误消息
            details: 错误详情
            status_code: HTTP状态码
        
        Returns:
            dict: 标准化的错误响应
        """
        response = {
            "success": False,
            "error": {
                "code": error_code,
                "message": message
            }
        }
        
        if details:
            response["error"]["details"] = details
        
        return response


async def error_handler_middleware(request: Request, call_next):
    """
    全局错误处理中间件
    
    捕获所有未处理的异常并返回标准化的错误响应
    """
    try:
        response = await call_next(request)
        return response
        
    except RequestValidationError as e:
        # 请求验证错误
        logger.warning(f"请求验证失败: {request.url} - {e}")
        
        error_details = []
        for error in e.errors():
            error_details.append({
                "field": " -> ".join(str(loc) for loc in error["loc"]),
                "message": error["msg"],
                "type": error["type"]
            })
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=ErrorResponse.format_error(
                error_code="VALIDATION_ERROR",
                message="请求参数验证失败",
                details=error_details,
                status_code=422
            )
        )
    
    except SQLAlchemyError as e:
        # 数据库错误
        logger.error(f"数据库错误: {request.url} - {e}")
        logger.error(traceback.format_exc())
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse.format_error(
                error_code="DATABASE_ERROR",
                message="数据库操作失败",
                details=str(e),
                status_code=500
            )
        )
    
    except ValueError as e:
        # 值错误（通常是业务逻辑错误）
        logger.warning(f"业务逻辑错误: {request.url} - {e}")
        
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse.format_error(
                error_code="BUSINESS_ERROR",
                message=str(e),
                status_code=400
            )
        )
    
    except PermissionError as e:
        # 权限错误
        logger.warning(f"权限错误: {request.url} - {e}")
        
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=ErrorResponse.format_error(
                error_code="PERMISSION_DENIED",
                message="没有权限执行此操作",
                details=str(e),
                status_code=403
            )
        )
    
    except FileNotFoundError as e:
        # 文件未找到
        logger.warning(f"文件未找到: {request.url} - {e}")
        
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse.format_error(
                error_code="FILE_NOT_FOUND",
                message="请求的文件不存在",
                details=str(e),
                status_code=404
            )
        )
    
    except Exception as e:
        # 未知错误
        logger.error(f"未知错误: {request.url} - {e}")
        logger.error(traceback.format_exc())
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse.format_error(
                error_code="INTERNAL_ERROR",
                message="服务器内部错误",
                details=str(e) if logger.level == logging.DEBUG else None,
                status_code=500
            )
        )


class APIException(Exception):
    """自定义API异常基类"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "API_ERROR",
        status_code: int = 500,
        details: Union[dict, list, str] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundException(APIException):
    """资源未找到异常"""
    
    def __init__(self, resource: str, identifier: str = None):
        message = f"{resource}不存在"
        if identifier:
            message += f": {identifier}"
        
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404
        )


class ValidationException(APIException):
    """验证异常"""
    
    def __init__(self, message: str, details: Union[dict, list] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=422,
            details=details
        )


class AuthenticationException(APIException):
    """认证异常"""
    
    def __init__(self, message: str = "认证失败"):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401
        )


class AuthorizationException(APIException):
    """授权异常"""
    
    def __init__(self, message: str = "没有权限执行此操作"):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403
        )


# 日志工具函数

def log_request(request: Request):
    """记录请求日志"""
    logger.info(f"请求: {request.method} {request.url}")


def log_response(response, duration: float):
    """记录响应日志"""
    logger.info(f"响应: {response.status_code} - 耗时: {duration:.3f}s")


def log_error(error: Exception, context: str = ""):
    """记录错误日志"""
    logger.error(f"错误 [{context}]: {error}")
    logger.error(traceback.format_exc())
